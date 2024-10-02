import os
import random
import sys
from typing import Sequence, Mapping, Any, Union
import torch


def get_value_at_index(obj: Union[Sequence, Mapping], index: int) -> Any:
    """Returns the value at the given index of a sequence or mapping.

    If the object is a sequence (like list or string), returns the value at the given index.
    If the object is a mapping (like a dictionary), returns the value at the index-th key.

    Some return a dictionary, in these cases, we look for the "results" key

    Args:
        obj (Union[Sequence, Mapping]): The object to retrieve the value from.
        index (int): The index of the value to retrieve.

    Returns:
        Any: The value at the given index.

    Raises:
        IndexError: If the index is out of bounds for the object and the object is not a mapping.
    """
    try:
        return obj[index]
    except KeyError:
        return obj["result"][index]


def find_path(name: str, path: str = None) -> str:
    """
    Recursively looks at parent folders starting from the given path until it finds the given name.
    Returns the path as a Path object if found, or None otherwise.
    """
    # If no path is given, use the current working directory
    if path is None:
        path = os.getcwd()

    # Check if the current directory contains the name
    if name in os.listdir(path):
        path_name = os.path.join(path, name)
        print(f"{name} found: {path_name}")
        return path_name

    # Get the parent directory
    parent_directory = os.path.dirname(path)

    # If the parent directory is the same as the current directory, we've reached the root and stop the search
    if parent_directory == path:
        return None

    # Recursively call the function with the parent directory
    return find_path(name, parent_directory)


def add_comfyui_directory_to_sys_path() -> None:
    """
    Add 'ComfyUI' to the sys.path
    """
    comfyui_path = find_path("ComfyUI")
    if comfyui_path is not None and os.path.isdir(comfyui_path):
        sys.path.append(comfyui_path)
        print(f"'{comfyui_path}' added to sys.path")


def add_extra_model_paths() -> None:
    """
    Parse the optional extra_model_paths.yaml file and add the parsed paths to the sys.path.
    """
    try:
        from main import load_extra_path_config
    except ImportError:
        print(
            "Could not import load_extra_path_config from main.py. Looking in utils.extra_config instead."
        )
        from utils.extra_config import load_extra_path_config

    extra_model_paths = find_path("extra_model_paths.yaml")

    if extra_model_paths is not None:
        load_extra_path_config(extra_model_paths)
    else:
        print("Could not find the extra_model_paths config file.")


add_comfyui_directory_to_sys_path()
add_extra_model_paths()


def import_custom_nodes() -> None:
    """Find all custom nodes in the custom_nodes folder and add those node objects to NODE_CLASS_MAPPINGS

    This function sets up a new asyncio event loop, initializes the PromptServer,
    creates a PromptQueue, and initializes the custom nodes.
    """
    import asyncio
    import execution
    from nodes import init_extra_nodes
    import server

    # Creating a new event loop and setting it as the default loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Creating an instance of PromptServer with the loop
    server_instance = server.PromptServer(loop)
    execution.PromptQueue(server_instance)

    # Initializing custom nodes
    init_extra_nodes()


from nodes import NODE_CLASS_MAPPINGS


def main():
    import_custom_nodes()
    with torch.inference_mode():
        loadimage = NODE_CLASS_MAPPINGS["LoadImage"]()
        loadimage_1 = loadimage.load_image(image="100588455.png")

        loadimage_2 = loadimage.load_image(image="background _image_with text.jpeg")

        cr_image_size = NODE_CLASS_MAPPINGS["CR Image Size"]()
        cr_image_size_7 = cr_image_size.ImageSize(
            width=1600, height=904, upscale_factor=1
        )

        checkpointloadersimple = NODE_CLASS_MAPPINGS["CheckpointLoaderSimple"]()
        checkpointloadersimple_264 = checkpointloadersimple.load_checkpoint(
            ckpt_name="epicrealism_naturalSinRC1VAE.safetensors"
        )

        cr_text = NODE_CLASS_MAPPINGS["CR Text"]()
        cr_text_583 = cr_text.text_multiline(
            text="Write text 'Independence Day Discount 20% off' on a sticker on the top right side of the image\n\nA plain and empty podium in a circular shape place in center. The background and style should be on this: \nA vibrant, patriotic scene of India celebrating Independence Day. Imagine a bustling city street filled with people waving flags, dancing, and wearing traditional attire. In the background, iconic Indian landmarks like the Taj Mahal or the Red Fort are bathed in the golden glow of the setting sun. The overall atmosphere should be festive, energetic, and full of national pride.\nThe product is a jar containing schezwan sauce with a white lid of company Chings\n\n"
        )

        cliptextencode = NODE_CLASS_MAPPINGS["CLIPTextEncode"]()
        cliptextencode_266 = cliptextencode.encode(
            text=get_value_at_index(cr_text_583, 0),
            clip=get_value_at_index(checkpointloadersimple_264, 1),
        )

        cliptextencode_269 = cliptextencode.encode(
            text="", clip=get_value_at_index(checkpointloadersimple_264, 1)
        )

        logic_boolean_primitive = NODE_CLASS_MAPPINGS["Logic Boolean Primitive"]()
        logic_boolean_primitive_629 = logic_boolean_primitive.do(boolean=True)

        cr_set_value_on_boolean = NODE_CLASS_MAPPINGS["CR Set Value On Boolean"]()
        cr_set_value_on_boolean_632 = cr_set_value_on_boolean.set_value(
            boolean=get_value_at_index(logic_boolean_primitive_629, 0),
            value_if_true=1,
            value_if_false=2,
        )

        imageresize = NODE_CLASS_MAPPINGS["ImageResize+"]()
        imageresize_8 = imageresize.execute(
            width=get_value_at_index(cr_image_size_7, 0),
            height=get_value_at_index(cr_image_size_7, 1),
            interpolation="lanczos",
            method="fill / crop",
            condition="always",
            multiple_of=0,
            image=get_value_at_index(loadimage_2, 0),
        )

        layercolor_exposure = NODE_CLASS_MAPPINGS["LayerColor: Exposure"]()
        layercolor_exposure_488 = layercolor_exposure.color_correct_exposure(
            exposure=1, image=get_value_at_index(imageresize_8, 0)
        )

        image_blank = NODE_CLASS_MAPPINGS["Image Blank"]()
        image_blank_627 = image_blank.blank_image(
            width=get_value_at_index(cr_image_size_7, 0),
            height=get_value_at_index(cr_image_size_7, 1),
            red=80,
            green=80,
            blue=80,
        )

        cr_image_input_switch = NODE_CLASS_MAPPINGS["CR Image Input Switch"]()
        cr_image_input_switch_610 = cr_image_input_switch.switch(
            Input=get_value_at_index(cr_set_value_on_boolean_632, 0),
            image1=get_value_at_index(layercolor_exposure_488, 0),
            image2=get_value_at_index(image_blank_627, 0),
        )

        imageresize_97 = imageresize.execute(
            width=get_value_at_index(cr_image_size_7, 0),
            height=get_value_at_index(cr_image_size_7, 1),
            interpolation="lanczos",
            method="pad",
            condition="always",
            multiple_of=0,
            image=get_value_at_index(loadimage_1, 0),
        )

        easy_imagerembg = NODE_CLASS_MAPPINGS["easy imageRemBg"]()
        easy_imagerembg_11 = easy_imagerembg.remove(
            rem_mode="RMBG-1.4",
            image_output="Preview",
            save_prefix="ComfyUI",
            torchscript_jit=False,
            images=get_value_at_index(imageresize_97, 0),
        )

        layercolor_exposure_294 = layercolor_exposure.color_correct_exposure(
            exposure=4, image=get_value_at_index(easy_imagerembg_11, 0)
        )

        layerutility_imageblendadvance_v2 = NODE_CLASS_MAPPINGS[
            "LayerUtility: ImageBlendAdvance V2"
        ]()
        layerutility_imageblendadvance_v2_360 = (
            layerutility_imageblendadvance_v2.image_blend_advance_v2(
                invert_mask=False,
                blend_mode="normal",
                opacity=100,
                x_percent=50,
                y_percent=60,
                mirror="None",
                scale=0.4,
                aspect_ratio=1,
                rotate=0,
                transform_method="lanczos",
                anti_aliasing=0,
                background_image=get_value_at_index(cr_image_input_switch_610, 0),
                layer_image=get_value_at_index(layercolor_exposure_294, 0),
            )
        )

        layercolor_autoadjust = NODE_CLASS_MAPPINGS["LayerColor: AutoAdjust"]()
        layercolor_autoadjust_99 = layercolor_autoadjust.auto_adjust(
            strength=10,
            brightness=0,
            contrast=0,
            saturation=0,
            red=0,
            green=0,
            blue=0,
            image=get_value_at_index(layerutility_imageblendadvance_v2_360, 0),
        )

        checkpointloadersimple_593 = checkpointloadersimple.load_checkpoint(
            ckpt_name="juggernautXL_v9Rdphoto2Lightning.safetensors"
        )

        loraloader = NODE_CLASS_MAPPINGS["LoraLoader"]()
        loraloader_594 = loraloader.load_lora(
            lora_name="mjv6.safetensors",
            strength_model=0.2,
            strength_clip=1,
            model=get_value_at_index(checkpointloadersimple_593, 0),
            clip=get_value_at_index(checkpointloadersimple_593, 1),
        )

        cliptextencode_595 = cliptextencode.encode(
            text=get_value_at_index(cr_text_583, 0),
            clip=get_value_at_index(loraloader_594, 1),
        )

        cliptextencode_598 = cliptextencode.encode(
            text="", clip=get_value_at_index(checkpointloadersimple_593, 1)
        )

        controlnetloader = NODE_CLASS_MAPPINGS["ControlNetLoader"]()
        controlnetloader_600 = controlnetloader.load_controlnet(
            control_net_name="SDXL\controlnet-canny-sdxl-1.0\diffusion_pytorch_model_V2.safetensors"
        )

        imagecompositemasked = NODE_CLASS_MAPPINGS["ImageCompositeMasked"]()
        imagecompositemasked_661 = imagecompositemasked.composite(
            x=0,
            y=0,
            resize_source=False,
            destination=get_value_at_index(image_blank_627, 0),
            source=get_value_at_index(layerutility_imageblendadvance_v2_360, 0),
            mask=get_value_at_index(layerutility_imageblendadvance_v2_360, 1),
        )

        cannyedgepreprocessor = NODE_CLASS_MAPPINGS["CannyEdgePreprocessor"]()
        cannyedgepreprocessor_602 = cannyedgepreprocessor.execute(
            low_threshold=100,
            high_threshold=200,
            resolution=1024,
            image=get_value_at_index(imagecompositemasked_661, 0),
        )

        controlnetapplyadvanced = NODE_CLASS_MAPPINGS["ControlNetApplyAdvanced"]()
        controlnetapplyadvanced_599 = controlnetapplyadvanced.apply_controlnet(
            strength=1,
            start_percent=0,
            end_percent=1,
            positive=get_value_at_index(cliptextencode_595, 0),
            negative=get_value_at_index(cliptextencode_598, 0),
            control_net=get_value_at_index(controlnetloader_600, 0),
            image=get_value_at_index(cannyedgepreprocessor_602, 0),
        )

        vaeencode = NODE_CLASS_MAPPINGS["VAEEncode"]()
        vaeencode_606 = vaeencode.encode(
            pixels=get_value_at_index(imagecompositemasked_661, 0),
            vae=get_value_at_index(checkpointloadersimple_593, 2),
        )

        ksampler = NODE_CLASS_MAPPINGS["KSampler"]()
        ksampler_597 = ksampler.sample(
            seed=random.randint(1, 2**64),
            steps=6,
            cfg=3,
            sampler_name="dpmpp_sde",
            scheduler="karras",
            denoise=1,
            model=get_value_at_index(loraloader_594, 0),
            positive=get_value_at_index(controlnetapplyadvanced_599, 0),
            negative=get_value_at_index(controlnetapplyadvanced_599, 1),
            latent_image=get_value_at_index(vaeencode_606, 0),
        )

        vaedecode = NODE_CLASS_MAPPINGS["VAEDecode"]()
        vaedecode_604 = vaedecode.decode(
            samples=get_value_at_index(ksampler_597, 0),
            vae=get_value_at_index(checkpointloadersimple_593, 2),
        )

        growmaskwithblur = NODE_CLASS_MAPPINGS["GrowMaskWithBlur"]()
        growmaskwithblur_333 = growmaskwithblur.expand_mask(
            expand=-1,
            incremental_expandrate=0,
            tapered_corners=True,
            flip_input=False,
            blur_radius=1,
            lerp_alpha=1,
            decay_factor=1,
            fill_holes=False,
            mask=get_value_at_index(layerutility_imageblendadvance_v2_360, 1),
        )

        imagecompositemasked_740 = imagecompositemasked.composite(
            x=0,
            y=0,
            resize_source=False,
            destination=get_value_at_index(vaedecode_604, 0),
            source=get_value_at_index(imagecompositemasked_661, 0),
            mask=get_value_at_index(growmaskwithblur_333, 0),
        )

        cr_image_input_switch_580 = cr_image_input_switch.switch(
            Input=get_value_at_index(cr_set_value_on_boolean_632, 0),
            image1=get_value_at_index(layercolor_autoadjust_99, 0),
            image2=get_value_at_index(imagecompositemasked_740, 0),
        )

        vaeencode_277 = vaeencode.encode(
            pixels=get_value_at_index(cr_image_input_switch_580, 0),
            vae=get_value_at_index(checkpointloadersimple_264, 2),
        )

        iclightconditioning = NODE_CLASS_MAPPINGS["ICLightConditioning"]()
        iclightconditioning_276 = iclightconditioning.encode(
            multiplier=0.18,
            positive=get_value_at_index(cliptextencode_266, 0),
            negative=get_value_at_index(cliptextencode_269, 0),
            vae=get_value_at_index(checkpointloadersimple_264, 2),
            foreground=get_value_at_index(vaeencode_277, 0),
        )

        cr_image_input_switch_613 = cr_image_input_switch.switch(
            Input=get_value_at_index(cr_set_value_on_boolean_632, 0),
            image1=get_value_at_index(layercolor_autoadjust_99, 0),
            image2=get_value_at_index(imagecompositemasked_740, 0),
        )

        image_select_channel = NODE_CLASS_MAPPINGS["Image Select Channel"]()
        image_select_channel_40 = image_select_channel.select_channel(
            channel="green", image=get_value_at_index(cr_image_input_switch_613, 0)
        )

        imageblur = NODE_CLASS_MAPPINGS["ImageBlur"]()
        imageblur_98 = imageblur.blur(
            blur_radius=30,
            sigma=1,
            image=get_value_at_index(image_select_channel_40, 0),
        )

        layercolor_brightness__contrast = NODE_CLASS_MAPPINGS[
            "LayerColor: Brightness & Contrast"
        ]()
        layercolor_brightness__contrast_549 = (
            layercolor_brightness__contrast.color_correct_brightness_and_contrast(
                brightness=1.2,
                contrast=1,
                saturation=1,
                image=get_value_at_index(imageblur_98, 0),
            )
        )

        vaeencode_284 = vaeencode.encode(
            pixels=get_value_at_index(layercolor_brightness__contrast_549, 0),
            vae=get_value_at_index(checkpointloadersimple_264, 2),
        )

        controlnetloader_301 = controlnetloader.load_controlnet(
            control_net_name="SDXL\controlnet-canny-sdxl-1.0\diffusion_pytorch_model_V2.safetensors"
        )

        loadandapplyiclightunet = NODE_CLASS_MAPPINGS["LoadAndApplyICLightUnet"]()
        loadandapplyiclightunet_279 = loadandapplyiclightunet.load(
            model_path="iclight_sd15_fc_unet_ldm.safetensors",
            model=get_value_at_index(checkpointloadersimple_264, 0),
        )

        ksampler_278 = ksampler.sample(
            seed=random.randint(1, 2**64),
            steps=40,
            cfg=3,
            sampler_name="dpmpp_2m_sde",
            scheduler="karras",
            denoise=1,
            model=get_value_at_index(loadandapplyiclightunet_279, 0),
            positive=get_value_at_index(iclightconditioning_276, 0),
            negative=get_value_at_index(iclightconditioning_276, 1),
            latent_image=get_value_at_index(vaeencode_284, 0),
        )

        vaedecode_280 = vaedecode.decode(
            samples=get_value_at_index(ksampler_278, 0),
            vae=get_value_at_index(checkpointloadersimple_264, 2),
        )

        color_blend = NODE_CLASS_MAPPINGS["Color Blend"]()
        color_blend_750 = color_blend.blend(
            mode="Luminosity",
            blend_image=get_value_at_index(vaedecode_280, 0),
            base_image=get_value_at_index(cr_image_input_switch_580, 0),
        )

        image_blend = NODE_CLASS_MAPPINGS["Image Blend"]()
        image_blend_755 = image_blend.image_blend(
            blend_percentage=0.1,
            image_a=get_value_at_index(color_blend_750, 0),
            image_b=get_value_at_index(vaedecode_280, 0),
        )

        checkpointloadersimple_325 = checkpointloadersimple.load_checkpoint(
            ckpt_name="juggernautXL_v9Rdphoto2Lightning.safetensors"
        )

        vaeencode_309 = vaeencode.encode(
            pixels=get_value_at_index(image_blend_755, 0),
            vae=get_value_at_index(checkpointloadersimple_325, 2),
        )

        loraloader_326 = loraloader.load_lora(
            lora_name="mjv6.safetensors",
            strength_model=0.2,
            strength_clip=1,
            model=get_value_at_index(checkpointloadersimple_325, 0),
            clip=get_value_at_index(checkpointloadersimple_325, 1),
        )

        cliptextencode_327 = cliptextencode.encode(
            text=get_value_at_index(cr_text_583, 0),
            clip=get_value_at_index(loraloader_326, 1),
        )

        cliptextencode_328 = cliptextencode.encode(
            text="", clip=get_value_at_index(loraloader_326, 1)
        )

        logic_boolean_primitive_649 = logic_boolean_primitive.do(boolean=True)

        unetloader = NODE_CLASS_MAPPINGS["UNETLoader"]()
        unetloader_773 = unetloader.load_unet(
            unet_name="flux1-schnell.safetensors", weight_dtype="default"
        )

        dualcliploader = NODE_CLASS_MAPPINGS["DualCLIPLoader"]()
        dualcliploader_774 = dualcliploader.load_clip(
            clip_name1="t5xxl_fp16.safetensors",
            clip_name2="clip_l.safetensors",
            type="flux",
        )

        cliptextencode_775 = cliptextencode.encode(
            text="A plain and empty wooden podium in a circular shape placed in a home drawing room with a small library and sofa background with soft diffused lightning designed  This scene should evoke a modern classy feeling",
            clip=get_value_at_index(dualcliploader_774, 0),
        )

        emptylatentimage = NODE_CLASS_MAPPINGS["EmptyLatentImage"]()
        emptylatentimage_777 = emptylatentimage.generate(
            width=1304, height=800, batch_size=1
        )

        randomnoise = NODE_CLASS_MAPPINGS["RandomNoise"]()
        randomnoise_778 = randomnoise.get_noise(noise_seed=random.randint(1, 2**64))

        ksamplerselect = NODE_CLASS_MAPPINGS["KSamplerSelect"]()
        ksamplerselect_780 = ksamplerselect.get_sampler(sampler_name="euler")

        vaeloader = NODE_CLASS_MAPPINGS["VAELoader"]()
        vaeloader_782 = vaeloader.load_vae(
            vae_name="diffusion_pytorch_model.safetensors"
        )

        detailtransfer = NODE_CLASS_MAPPINGS["DetailTransfer"]()
        restoredetail = NODE_CLASS_MAPPINGS["RestoreDetail"]()
        layercolor_coloradapter = NODE_CLASS_MAPPINGS["LayerColor: ColorAdapter"]()
        layermask_maskpreview = NODE_CLASS_MAPPINGS["LayerMask: MaskPreview"]()
        image_comparer_rgthree = NODE_CLASS_MAPPINGS["Image Comparer (rgthree)"]()
        splitimagewithalpha = NODE_CLASS_MAPPINGS["SplitImageWithAlpha"]()
        basicguider = NODE_CLASS_MAPPINGS["BasicGuider"]()
        basicscheduler = NODE_CLASS_MAPPINGS["BasicScheduler"]()
        samplercustomadvanced = NODE_CLASS_MAPPINGS["SamplerCustomAdvanced"]()
        saveimage = NODE_CLASS_MAPPINGS["SaveImage"]()

        for q in range(1):
            cr_set_value_on_boolean_650 = cr_set_value_on_boolean.set_value(
                boolean=get_value_at_index(logic_boolean_primitive_649, 0),
                value_if_true=1,
                value_if_false=2,
            )

            cannyedgepreprocessor_415 = cannyedgepreprocessor.execute(
                low_threshold=100,
                high_threshold=200,
                resolution=1024,
                image=get_value_at_index(image_blend_755, 0),
            )

            controlnetapplyadvanced_414 = controlnetapplyadvanced.apply_controlnet(
                strength=1,
                start_percent=0,
                end_percent=1,
                positive=get_value_at_index(cliptextencode_327, 0),
                negative=get_value_at_index(cliptextencode_328, 0),
                control_net=get_value_at_index(controlnetloader_301, 0),
                image=get_value_at_index(cannyedgepreprocessor_415, 0),
            )

            ksampler_304 = ksampler.sample(
                seed=random.randint(1, 2**64),
                steps=3,
                cfg=2,
                sampler_name="dpmpp_sde",
                scheduler="karras",
                denoise=0.4,
                model=get_value_at_index(loraloader_326, 0),
                positive=get_value_at_index(controlnetapplyadvanced_414, 0),
                negative=get_value_at_index(controlnetapplyadvanced_414, 1),
                latent_image=get_value_at_index(vaeencode_309, 0),
            )

            vaedecode_305 = vaedecode.decode(
                samples=get_value_at_index(ksampler_304, 0),
                vae=get_value_at_index(checkpointloadersimple_325, 2),
            )

            cr_image_input_switch_704 = cr_image_input_switch.switch(
                Input=get_value_at_index(cr_set_value_on_boolean_650, 0),
                image1=get_value_at_index(vaedecode_305, 0),
                image2=get_value_at_index(image_blend_755, 0),
            )

            detailtransfer_290 = detailtransfer.process(
                mode="soft_light",
                blur_sigma=5,
                blend_factor=1,
                target=get_value_at_index(cr_image_input_switch_704, 0),
                source=get_value_at_index(layercolor_autoadjust_99, 0),
                mask=get_value_at_index(growmaskwithblur_333, 0),
            )

            restoredetail_714 = restoredetail.batch_normalize(
                mode="add",
                blur_type="blur",
                blur_size=5,
                factor=1,
                images=get_value_at_index(image_blend_755, 0),
                detail=get_value_at_index(detailtransfer_290, 0),
            )

            cr_image_input_switch_559 = cr_image_input_switch.switch(
                Input=get_value_at_index(cr_set_value_on_boolean_632, 0),
                image1=get_value_at_index(layercolor_autoadjust_99, 0),
                image2=get_value_at_index(imagecompositemasked_740, 0),
            )

            layercolor_coloradapter_287 = layercolor_coloradapter.color_adapter(
                opacity=50,
                image=get_value_at_index(restoredetail_714, 0),
                color_ref_image=get_value_at_index(cr_image_input_switch_559, 0),
            )

            layermask_maskpreview_486 = layermask_maskpreview.mask_preview(
                mask=get_value_at_index(growmaskwithblur_333, 0)
            )

            image_comparer_rgthree_757 = image_comparer_rgthree.compare_images(
                image_a=get_value_at_index(vaedecode_305, 0),
                image_b=get_value_at_index(image_blend_755, 0),
            )

            splitimagewithalpha_763 = splitimagewithalpha.split_image_with_alpha(
                image=get_value_at_index(loadimage_1, 0)
            )

            image_comparer_rgthree_768 = image_comparer_rgthree.compare_images(
                image_a=get_value_at_index(image_blend_755, 0),
                image_b=get_value_at_index(cr_image_input_switch_580, 0),
            )

            image_blend_770 = image_blend.image_blend(
                blend_percentage=0.6,
                image_a=get_value_at_index(layercolor_coloradapter_287, 0),
                image_b=get_value_at_index(detailtransfer_290, 0),
            )

            basicguider_776 = basicguider.get_guider(
                model=get_value_at_index(unetloader_773, 0),
                conditioning=get_value_at_index(cliptextencode_775, 0),
            )

            basicscheduler_783 = basicscheduler.get_sigmas(
                scheduler="sgm_uniform",
                steps=20,
                denoise=1,
                model=get_value_at_index(unetloader_773, 0),
            )

            samplercustomadvanced_781 = samplercustomadvanced.sample(
                noise=get_value_at_index(randomnoise_778, 0),
                guider=get_value_at_index(basicguider_776, 0),
                sampler=get_value_at_index(ksamplerselect_780, 0),
                sigmas=get_value_at_index(basicscheduler_783, 0),
                latent_image=get_value_at_index(emptylatentimage_777, 0),
            )

            vaedecode_785 = vaedecode.decode(
                samples=get_value_at_index(samplercustomadvanced_781, 0),
                vae=get_value_at_index(vaeloader_782, 0),
            )

            saveimage_784 = saveimage.save_images(
                filename_prefix="ComfyUI", images=get_value_at_index(vaedecode_785, 0)
            )


if __name__ == "__main__":
    main()
