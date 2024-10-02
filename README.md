# PromoGenie

                 Unleashing Creativity, One Banner at a Time!

This repository contains a Comfy workflow for advanced product photography enhancement. The workflow combines AI-powered background generation, product isolation, and image compositing to create professional-looking product images.

## Results

![results](./Assets/Output%20Images/Chings%20Independence%20day%2020%20off.png)

![results](./Assets/Output%20Images/Diwali%20flat%20100%20off.png)

![results](./Assets/Output%20Images/juice%20image.jpg)

![results](./Assets/Output%20Images/gillitte_jaguar.png)

![results](./Assets/Output%20Images/soda%20can.png)

## Architecture

![architecture](./Assets/Architecture/Architecture%20Diagram.png)

The architecture explains that the user will interact with the workflow and the workflow will generate the output. The interaction is done via web app powered by Google's Gemini Model. The models are hosted on Google Cloud servers and the data is being stored at each step at Google Cloud storage

## Workflow Overview

Worflow file can be found here: [workflow](./workflow_bb_product.json)

Python script of the workflow can be found here: [python script](./workflow_bb_product.py)


The process consists of three main steps:

1. Prompt Generation
2. Background Image Creation
3. Product Image Compositing

### 1. Prompt Generation

![prompt](./Assets/Workflow%20Diagram/1.%20Gemini%20for%20Prompt%20Generation.png)

- Utilizes Google's Gemini API for interactive prompt creation
- User converses with the AI to refine and finalize a prompt for the background image
- Sample Prompts are:
  - Diwali Prompt: `A magical, illuminated cityscape during Diwali. Imagine a bustling Indian city transformed into a wonderland of light. Buildings are adorned with intricate rangoli patterns and shimmering lanterns. The sky is ablaze with fireworks, casting colorful reflections on the city's streets. The overall atmosphere should be festive, joyous, and filled with the warmth of celebration.`
  - Independence Day Prompt: `A vibrant, patriotic scene of India celebrating Independence Day. Imagine a bustling city street filled with people waving flags, dancing, and wearing traditional attire. In the background, iconic Indian landmarks like the Taj Mahal or the Red Fort are bathed in the golden glow of the setting sun. The overall atmosphere should be festive, energetic, and full of national pride.`

### 2. Background Image Creation

![background](./Assets/Workflow%20Diagram/2.%20Flux%20model%20to%20generate%20background%20images.png)

- Takes the finalized prompt from step 1
- Adds promotional elements and sets image dimensions
- Uses the Flux Dev model to generate a variety of background options
- Selects the best background for further processing

- Sample Generated Backgrounds:
  - Diwali Prompt: `Write a text "Flat ₹100 off" on a sticker on the top right side of the image.\n\n A plain and empty stool in a circular shape placed in centre. The stool should be empty.  The background and style should be on this: A magical, illuminated cityscape during Diwali. Imagine a bustling Indian city transformed into a wonderland of light. Buildings are adorned with intricate rangoli patterns and shimmering lanterns. The sky is ablaze with fireworks, casting colorful reflections on the city's streets. The overall atmosphere should be festive, joyous, and filled with the warmth of celebration.`
  - Sample Diwal Images:
  

 Diwali | Backgrounds
 -|-
![diwali_1](./Assets/Background%20Variations/diwali_1.jpeg) | ![diwali_2](./Assets/Background%20Variations/diwali_2.jpeg)
![diwali_3](./Assets/Background%20Variations/diwali_3.jpeg) | ![diwali_4](./Assets/Background%20Variations/diwali_4.jpeg)

  - Independence Day Prompt: `Write a text "20% off" on the top right side of the image A plain and empty podium in a circular shape place in center. The background and style should be on this: A vibrant, patriotic scene of India celebrating Independence Day. Imagine a bustling city street filled with people waving flags, dancing, and wearing traditional attire. In the background, iconic Indian landmarks like the Taj Mahal or the Red Fort are bathed in the golden glow of the setting sun. The overall atmosphere should be festive, energetic, and full of national pride.`
  
  - Sample Independence Day Images:

 Diwali | Backgrounds
 -|-
![independence_1](./Assets/Background%20Variations/independence_1.jpeg) | ![independence_2](./Assets/Background%20Variations/independence_2.jpeg)
![independence_3](./Assets/Background%20Variations/independence_3.jpeg) | ![independence_4](./Assets/Background%20Variations/independence_4.jpeg)

From here the best background was number 4 image and that was selected.

### 3. Product Image Compositing

This step is divided into several sub-steps:

a. **Image Loading**

![image Loading](./Assets/Workflow%20Diagram/3.%20Control%20panel%20for%20all%20the%20nodes.png)
   - Loads the input product image and the generated background

   - Incorporates the prompt from step 2 along with product details

b. **Background Extraction**

![background extraction](./Assets/Workflow%20Diagram/4.%20Background%20removal%20and%20resizing.png)
   - Removes the background from the product image using BRIA Background Removal 1.4 Model
   - If no background exists, the original image is used
   - Rescales the background image if necessary
 - Background extraction from images having background:
  
  ![background_extraction_1](./Assets/Background%20Removal/Green%20Soda%20Can.png)

  Here we can see the can had a green background very similar to the color of the can, but it was easily extracted.

  ![background_extraction_1](./Assets/Background%20Removal/bb%20gillette%20and%20jaguar%20advt.png)

  Here we can see the background extraction from a jaguar Gillette advertisement given as a sample banner by Big Basket. This shows that we isolate objects from the existing banners as well.


c. **Image Projection**

![image projection](./Assets/Workflow%20Diagram/5.%20Location%20placement%20of%20Product.png)
   - Projects the product onto the new background
   - Performs various image operations:
     - Image blending
     - Color adjustment
     - Masking
     - Blurring
     - Brightness and contrast correction

- Can re adjust the product position based on the background. 

![product_adjustment](./Assets/Product%20Adjustment/product_adjustment_1.png)

Here we can see the the product is 53% on X and Y therefore not in the center like other images as the table in the background was not centered.

d. **Optional Background Regeneration**

![background_regeneration](./Assets/Workflow%20Diagram/6.%20Background%20Image%20generator%20from%20prompt%20and%20reference%20image.png)

   - Allows users to generate a new background using the prompt and existing background as reference
   - Utilizes ksampler and image generation models for composition.
  

e. **Relighting**

![relighting](./Assets/Workflow%20Diagram/7.%20Relighting%20the%20generating%20image.png)

   - Uses Epicrealism model and iclight_sd15_fc_unet_ldm model
   - Performs illumination operations based on the prompt and image
   - Applies color blending and image blending

**Note: Here we can see that the depth is being added as we look at the generated image at the last in the above screemshot. the lighting has added shadow which was absent making it more realistic.**


f. **Optional Repainting**

![repainting](./Assets/Workflow%20Diagram/8.%20Repaining%20the%20image%20for%20better%20lighting.png)

   - For users unsatisfied with the lighting results
   - Creates variations based on the previous generated image and prompt
   - Utilizes ControlNet Canny Edge to preserve object details

g. **Final Compositing**

![final_compositing](./Assets/Workflow%20Diagram/9.%20Repaining%20the%20image%20for%20better%20lighting.png)
   - Blends the original product image over the processed background
   - Applies color adaptation to match lighting conditions.
  
 **Note: From the output generatd from the aboove steps we could see that the text over the product was not looking good as well as at some places the color of the product got changed. Here in this step we have almost retrained everything.**

## Video walkthrough

The video link can be found here: [link](https://drive.google.com/drive/folders/1Dttyh-qvbc-gkHBUURdJ3uVL5xij61rb)