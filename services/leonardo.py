import requests
import time
from typing import Dict

class LeonardoAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://cloud.leonardo.ai/api/rest/v1"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

    def _get_base_payload(self, prompt: str) -> Dict:
        return {
            "prompt": prompt,
            "modelId": "aa77f04e-3eec-4034-9c07-d0f619684628",
            "width": 1024,
            "height": 1024,
            "alchemy": True,
            "photoReal": True,
            "photoRealVersion": "v2",
            "presetStyle": "CINEMATIC",
            "num_images": 1
        }

    def generate_image(self, prompt: str) -> Dict:
        try:
            payload = self._get_base_payload(prompt)
            response = requests.post(
                f"{self.base_url}/generations",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            
            if 'sdGenerationJob' in response.json():
                generation_id = response.json()['sdGenerationJob']['generationId']
                return self._wait_for_generation(generation_id)
            
            return {"error": "Invalid response format"}
            
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def _wait_for_generation(self, generation_id: str, max_attempts: int = 30) -> Dict:
        for _ in range(max_attempts):
            try:
                response = requests.get(
                    f"{self.base_url}/generations/{generation_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                result = response.json()
                
                if 'generations_by_pk' in result:
                    generation = result['generations_by_pk']
                    if generation['status'] == 'COMPLETE':
                        return {
                            'url': generation['generated_images'][0]['url'],
                            'seed': generation['generated_images'][0].get('seed'),
                            'modelId': generation.get('modelId')
                        }
                    elif generation['status'] == 'FAILED':
                        return {
                            'error': 'Generation failed',
                            'details': generation.get('message', 'Unknown error')
                        }
            except Exception as e:
                print(f"Error checking generation status: {str(e)}")
            time.sleep(2)
        
        return {"error": "Generation timed out"}

    generate_marketing_image = generate_image  # They use the same logic in your code