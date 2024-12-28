import asyncio
import aiohttp
import time
import json
import statistics
import argparse
import base64
from datetime import datetime

class StressTest:
    def __init__(self, endpoint_id, api_key, num_users, num_requests, payload_file):
        self.endpoint_id = endpoint_id
        self.api_key = api_key
        self.num_users = num_users
        self.num_requests = num_requests
        self.payload_file = payload_file
        self.url = f"https://api.runpod.ai/v2/{endpoint_id}/runsync"
        self.results = []
        self.success_count = 0
        self.failure_count = 0
        self.start_time = None
        self.end_time = None

    def load_payload(self):
        try:
            with open(self.payload_file, 'rb') as f:
                image_bytes = f.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                return {
                    "input": {
                        "image": image_base64,
                        "box_threshold": 0.05,
                        "iou_threshold": 0.1
                    }
                }
        except Exception as e:
            print(f"Error loading payload file: {e}")
            raise

    async def make_request(self, session, user_id, request_id):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {self.api_key}',
            'content-type': 'application/json',
            'priority': 'u=1, i'
        }

        payload = self.load_payload()
        start_time = time.time()

        try:
            async with session.post(self.url, json=payload, headers=headers) as response:
                end_time = time.time()
                response_time = end_time - start_time
                
                if response.status == 200:
                    self.success_count += 1
                else:
                    self.failure_count += 1
                    print(f"Request failed with status {response.status}: {await response.text()}")

                self.results.append({
                    'user_id': user_id,
                    'request_id': request_id,
                    'response_time': response_time,
                    'status_code': response.status
                })

        except Exception as e:
            print(f"Error making request: {e}")
            self.failure_count += 1

    async def user_task(self, user_id):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(self.num_requests):
                task = asyncio.create_task(
                    self.make_request(session, user_id, i)
                )
                tasks.append(task)
            await asyncio.gather(*tasks)

    async def run(self):
        self.start_time = time.time()
        tasks = []
        for i in range(self.num_users):
            task = asyncio.create_task(self.user_task(i))
            tasks.append(task)
        await asyncio.gather(*tasks)
        self.end_time = time.time()
        self.print_results()

    def print_results(self):
        total_requests = self.num_users * self.num_requests
        total_time = self.end_time - self.start_time
        response_times = [r['response_time'] for r in self.results]
        
        print("\n=== Stress Test Results ===")
        print(f"Total Requests: {total_requests}")
        print(f"Successful Requests: {self.success_count}")
        print(f"Failed Requests: {self.failure_count}")
        print(f"Total Time: {total_time:.2f} seconds")
        print(f"Requests/Second: {total_requests/total_time:.2f}")
        print(f"Average Response Time: {statistics.mean(response_times):.2f} seconds")
        print(f"Median Response Time: {statistics.median(response_times):.2f} seconds")
        print(f"Min Response Time: {min(response_times):.2f} seconds")
        print(f"Max Response Time: {max(response_times):.2f} seconds")
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"stress_test_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump({
                'config': {
                    'endpoint_id': self.endpoint_id,
                    'num_users': self.num_users,
                    'num_requests': self.num_requests,
                },
                'metrics': {
                    'total_requests': total_requests,
                    'successful_requests': self.success_count,
                    'failed_requests': self.failure_count,
                    'total_time': total_time,
                    'requests_per_second': total_requests/total_time,
                    'avg_response_time': statistics.mean(response_times),
                    'median_response_time': statistics.median(response_times),
                    'min_response_time': min(response_times),
                    'max_response_time': max(response_times)
                },
                'raw_results': self.results
            }, f, indent=2)
        print(f"\nDetailed results saved to {results_file}")

def main():
    parser = argparse.ArgumentParser(description='RunPod API Stress Test')
    parser.add_argument('--endpoint-id', required=True, help='RunPod endpoint ID')
    parser.add_argument('--api-key', required=True, help='RunPod API key')
    parser.add_argument('--users', type=int, default=10, help='Number of concurrent users')
    parser.add_argument('--requests', type=int, default=100, help='Number of requests per user')
    parser.add_argument('--payload', required=True, help='Path to image file')
    
    args = parser.parse_args()
    
    stress_test = StressTest(
        args.endpoint_id,
        args.api_key,
        args.users,
        args.requests,
        args.payload
    )
    
    asyncio.run(stress_test.run())

if __name__ == "__main__":
    main() 