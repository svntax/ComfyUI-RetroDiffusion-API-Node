# ComfyUI-RetroDiffusion-API-Node

A ComfyUI custom node for the [Retro Diffusion API](https://retrodiffusion.ai/)

<img width="795" height="541" alt="comfyui_retrodiffusion_api_node showcase" src="https://github.com/user-attachments/assets/9f2c9634-74e6-4b61-a8f2-6e08132f2f4c" />

## How to Install
1. Go to [Retro Diffusion](https://retrodiffusion.ai/) and sign up for an account if you don't have one.
2. Create an API key from the developer tools.
3. In the root folder of your ComfyUI installation, create a `.env` file if it doesn't exist already.
4. Add the following to your `.env`:
```
RD_API_KEY=your-key
```
5. Clone this repository into your `ComfyUI/custom_nodes` folder.
6. Start ComfyUI.

Now you can create a `Retro Diffusion API Node` in your workflows.

## Features
- Text-to-image and image-to-image
- Outputs credit cost of the image and your remaining credits too
- Supports `RD_Fast`, `RD_PLUS`, and `Animation` styles as of the latest commit

More info on the Retro Diffusion API itself can be found here - https://github.com/Retro-Diffusion/api-examples

## Notes
- `RD_PLUS` and `Animation` styles are more expensive to generate than `RD_Fast`. 
- Check the console if you get any errors, and feel free to create an issue.
- There is an upload size limit for image-to-image, so keep that in mind (don't send large images as input).
