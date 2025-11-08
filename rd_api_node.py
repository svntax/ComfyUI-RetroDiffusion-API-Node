from PIL import Image
import numpy as np
import torch
import base64
from io import BytesIO
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def base64_to_image(base64_string):
    # Convert to PIL image
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    image = image.convert("RGB")
    
    # Convert to tensor format
    image_tensor = torch.from_numpy(np.array(image)).float() / 255.0
    image_tensor = image_tensor.unsqueeze(0)

    return image_tensor

def image_to_base64(image_input):
    # Convert from tensor format
    image_np = image_input.squeeze(0).numpy() * 255.0
    image_np = image_np.clip(0, 255).astype(np.uint8)
    
    # Convert to PIL image
    image = Image.fromarray(image_np, 'RGB')
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    
    image_bytes = buffer.getvalue()

    base64_string = base64.b64encode(image_bytes).decode('utf-8')

    return base64_string

class RetroDiffusionAPINode:
    @classmethod
    def INPUT_TYPES(cls):
        prompt_styles = ["rd_fast__default", "rd_fast__retro", "rd_fast__simple","rd_fast__detailed",
                         "rd_fast__anime", "rd_fast__game_asset", "rd_fast__portrait", "rd_fast__texture",
                         "rd_fast__ui", "rd_fast__item_sheet", "rd_fast__character_turnaround", "rd_fast__1_bit",
                         "rd_fast__low_res", "rd_fast__mc_item", "rd_fast__mc_texture", "rd_fast__no_style",
                         "rd_plus__default", "rd_plus__retro", "rd_plus__watercolor", "rd_plus__textured",
                         "rd_plus__cartoon", "rd_plus__ui_element", "rd_plus__item_sheet", "rd_plus__character_turnaround",
                         "rd_plus__topdown_map", "rd_plus__topdown_asset", "rd_plus__isometric", "rd_plus__isometric_asset",
                         "rd_plus__classic", "rd_plus__low_res", "rd_plus__mc_item", "rd_plus__mc_texture",
                         "rd_plus__topdown_item", "rd_plus__skill_icon", "rd_plus__environment",
                         "animation__four_angle_walking", "animation__walking_and_idle", "animation__small_sprites", "animation__vfx"]
        return {
            "required": {
                #"api_key": ("STRING", {"default": "YOUR_API_KEY", "multiline": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2147483647, "step": 1}),
                "width": ("INT", {"default": 128, "min": 16, "max": 512, "step": 8}),
                "height": ("INT", {"default": 128, "min": 16, "max": 512, "step": 8}),
                "prompt_style": (prompt_styles,),
                "bypass_prompt_expansion": ("BOOLEAN", {"default": False}),
                "remove_bg": ("BOOLEAN", {"default": False}),
                "tile_x": ("BOOLEAN", {"default": False}),
                "tile_y": ("BOOLEAN", {"default": False}),
                "return_spritesheet_for_animations": ("BOOLEAN", {"default": True}),
                #"num_images": ("INT", {"default": 1, "min": 1, "max": 16, "step": 1}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01})
            },
            "optional": {
                "input_image": ("IMAGE",)
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "credit_cost", "remaining_credits")
    FUNCTION = "generate_image"
    CATEGORY = "RetroDiffusion"

    def generate_image(self, seed, width, height, prompt_style, bypass_prompt_expansion, remove_bg, tile_x, tile_y, return_spritesheet_for_animations, prompt, denoise, input_image=None):
        url = "https://api.retrodiffusion.ai/v1/inferences"
        
        headers = {
            "X-RD-Token": os.getenv("RD_API_KEY"),
        }

        payload = {
            "seed": seed,
            "width": width,
            "height": height,
            "prompt_style": prompt_style,
            "bypass_prompt_expansion": bypass_prompt_expansion,
            "remove_bg": remove_bg,
            "tile_x": tile_x,
            "tile_y": tile_y,
            "return_spritesheet": return_spritesheet_for_animations,
            "prompt": prompt,
            "num_images": 1,
        }

        if input_image is not None:
            payload["input_image"] = image_to_base64(input_image)
            payload["strength"] = denoise

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Extract response info
            credit_cost = data.get("credit_cost", 0)
            print(f"Credit cost: {credit_cost}")
            remaining_credits = data.get("remaining_credits", 0)
            print(f"Remaining credits: {remaining_credits}")
            
            # Handle base64 image
            base64_images = data.get("base64_images", [])
            if not base64_images:
                raise ValueError("No images returned from RetroDiffusion API")
            
            # Convert base64 to image
            base64_image = base64_images[0] # Take first image
            image_tensor = base64_to_image(base64_image)
            
            return (image_tensor, credit_cost, remaining_credits)
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            # Return empty tensor and 0 cost on error
            return (torch.zeros(1, 64, 64, 3), 0, -1)
        except Exception as e:
            print(f"Error processing response: {e}")
            # Return empty tensor and 0 cost on error
            return (torch.zeros(1, 64, 64, 3), 0, -1)
