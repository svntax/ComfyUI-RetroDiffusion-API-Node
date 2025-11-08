# Retro Diffusion API Node

This node enables you to send image generation requests to [Retro Diffusion API](https://retrodiffusion.ai/)

A Retro Diffusion account and API key is required.

## Parameters

- **seed**: The random seed used for Retro Diffusion's inference
- **width**: The output width in pixels
- **height**: The output height in pixels
- **prompt_style**: The [style](https://github.com/Retro-Diffusion/api-examples?tab=readme-ov-file#using-styles) to use from Retro Diffusion
- **bypass_prompt_expansion**: Disable the prompt expansion that Retro Diffusion applies to your prompt when sending a request
- **remove_bg**: Enable Retro Diffusion's [background removal](https://github.com/Retro-Diffusion/api-examples?tab=readme-ov-file#using-background-removal-for-transparent-images)
- **tile_x**: Enable Retro Diffusion's seamless tiling effect along the x-axis
- **tile_y**: Enable Retro Diffusion's seamless tiling effect along the y-axis
- **return_spritesheet_for_animations**: Set the output of animation styles to a transparent PNG with the spritesheet instead of a transparent GIF
- **prompt**: The prompt for the image
- **denoise**: The amount of denoising applied
- **input_image**: An optional image used for img2img, or as a reference image for animation styles

## Usage

![example usage](https://github.com/user-attachments/assets/9f2c9634-74e6-4b61-a8f2-6e08132f2f4c)