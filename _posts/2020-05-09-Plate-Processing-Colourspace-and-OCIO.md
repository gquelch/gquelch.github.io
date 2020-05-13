---
title: Plate Processing - Colourspace and OCIO
layout: post
published: true
---

When working on any VFX project we want to keep consistent colour and quality of the plate throughout the pipeline, it's important to know how to get your footage imported and exported properly between softwares. Some projects require delivery in the exact same colourspace they came in, this means reciving the plate, converting it to a working colourspace to add our CG, and then being able to un-do that conversion. DaVinci Resolve offers great, visual control over what is happening to our footage. Some jobs however this is not nessecary, and we can deliver our own grade straight out of Nuke.


This guide is not applicable for ACES, but will work with OCIO configs such as [Filmic Blender](https://sobotka.github.io/filmic-blender/) and [SPI-Anim](https://github.com/imageworks/OpenColorIO-Configs/tree/master/spi-anim), as well as the standard Linear + sRGB workflow

# Importing the Plate

The first step will be to import the plate, this will usually be a video file, potentially an .mxf or .mov

- Bring plate into Resolve Media Tab, its as simple as dragging footage over the window. You'll probably get a popup asking you to change the project settings, I ususally press yes to this, but double check it later.

    From this we can create our timeline, right click on the footage, and select "Create New Timeline Using Selected Clips..."

    This will prompt us to give the timeline a name, I usually stick to a project code such as "PRJ\_seq#\_shot#\_" or "PRJ\_shot#\_"

    e.g. GUI\_001\_010\_ for project Guide, sequence 1, shot 1

    But name it whatever you feel is appropriate

    It's important to add the "\_" at the end, as this will seperate our name from our frame padding when we export

    Now is the time to check our project and timeline settings are correct, we do this in *File → Project Settings* You want to check the frame rate, pixel aspect ratio and resolution are correct

- You now want to go to the edit tab, at the bottom of your screen, you should be presented with a timeline, where you can trim your shot to the appropriate length

## Initial Colourspace

The next step is to do the conversion of the plate to linear colourspace, this is so we are in the same working space as our CG, we do this, in the colour tab

- We want to convert from our *Camera Colourspace → Linear* (e.g. CLog, sLog2 etc)

    As you would guess, camera colourspace varies by manufacturer, Arri uses CLog, Sony most often uses sLog2 or sLog3, you should be able to find this information online, from your footage metadata, or ideally from the DOP or a camera operator

    By default, Resolve will give us one node in our node graph, we can pick a LUT to do the conversion by right clicking on the node, and picking the appropriate one from *LUTs → 3D LUT → VFX IO*

    As you can see there are many options, so make sure you're using the correct one for your camera

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled.png" class = "responsive-image"/>

## Exporting from Resolve

Now we want to export our plate, I usually do 2 exports, one for the Lighting and Compositing artists, as Linear EXRs, and a proxy export, and for the animators, as a Linear TIF sequence.

Linear TIFs are a slightly odd decision, as any software will display them wrong by default, because it will assume that a TIF is already in sRGB. It does however mean that we do not have to create two timelines in Resolve, meaning changes to the edit or frame padding are simpler, this is really up to you.

We export from Resolve using the Delivery tab, you can queue up both exports at the same time

### File Settings

- "Timeline name" which keeps our exports consistent with our timeline namings
- 4 frame padding is usually plenty, but up it if you need
- I usually start each clip from 100, but if you need more pre-roll, you can start from 1000

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled%201.png" class = "responsive-image"/>

### Video Settings - EXR

- Half (16Bit) is usually plenty of bit depth for camera footage, which is often 10 or 12Bit, but check the quality of your footage, if you are unsure, RGB half will likely be plenty
- Our resolution, and framerate should be correct, based on our project settings
- Sometimes we may need to set our project to Cinemascope (2:1) aspect ratio, if this is an Anamorphic Project

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled%202.png" class = "responsive-image"/>

### Video Settings - TIF

- We want to pick RGB 8Bit with LZW Compression, as the quality is high but file size will be kept low
- For the TIF export we want to either half or quarter the Resolution, to keep fast file playback for the animators

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled%203.png" class = "responsive-image"/>

## Creating LUTs

Our final step for processing the plate is to create a Viewing LUT. Although our footage was filmed in a flat colourspace, when it is shot it will have most likely been displayed in Rec 709, but we don't simply want to go from *Plate Colourspace → Rec709* as in Nuke we are working in Linear. So we must create a LUT that takes us from *Linear → Plate Colourspace → Rec709*

I usually will re-import my EXR sequence into Resolve, in order to compare with a *Plate Colourspace → Rec709* on the original plate, to check they match, but you don't have to do this

- Again, using the right click menu in the colour tab, we want to create one node that converts us from *Linear → Plate Colourspace*
- We can create a second node using *Alt+s* on this node, we want to convert from *Plate Colourspace → Rec709*

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled%204.png" class = "responsive-image"/>

- We can now export this LUT buy right clicking on the thumbnail in the timeline, and pressing "Generate 3D LUT"

    I usually name it the same as the conversion I am doing, for example "*Linear\_Arri\_Rec709"*

We should now have the following:

- A Linear EXR sequence, for Lighting and Compositing
- A Linear TIF sequence, for Animation
- A Viewing LUT, for correctly displaying our footage in Nuke

---

# Maya Setup

## Lighting

Using Redshift, we can see our plate in the render by using the Back-Plate function on a DomeLight. This will allow us to see our CG on top of the plate, which makes the lighting process much more interactive

We can also make use of Shadow Materials in redshift in order to cast shadows onto the plate, directly in render, however this will be covered in another guide

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled%205.png" class = "responsive-image"/>

Redshift Dome Light

## Animation

At this stage we need to bare in mind Lens Distortion, the animators should work on the un-distorted plate, meaning that we should run our TIF sequence through an STMap or Lens Distort node in order to remove it

Once we have un-distorted our plate, we simply load the TIF sequence in as an Image Plane to our camera, one thing to remember is to change the Colourspace of the image plane, to "*Raw*" unless you have converted the plate to sRGB during the Lens Distortion phase

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled%206.png" class = "responsive-image"/>

Image Plane

---

# Nuke Setup

- Bring the plate into Nuke as a standard Linear EXR, nuke will then convert this to sRGB, it will give us a nice contrasty result, that we can work with
- We can use a Vectorfield Node to laod in our *Linear → Plate Colourspace → Rec 709* LUT
- Your image will now appear quite washed out, this is because the LUT left our image in Rec 709, and Nuke is adding sRGB on top of this, doubling up our colour transform
- To fix this, create an OCIO colourspace node and set it to in: sRGB, out: Linear

Im not sure why we need to set in sRGB in the OCIO colourspace, rather than Rec 709, but I've found that sRGB was the setting that matched Resolve

We may also be able to create a *Linear → Plate Colourspace → Rec 709 → Linear* LUT in Resolve, but I have not yet tested this workflow

You can now compare the image with and without our colour transforms, you'll notice slight difference between the two, which is to be expected. You can work look at either view, it is often good to compare work under different LUTs and grades to see how it is working, but ultimately its good to check against the LUT as this may be the starting point for the grade, and is what the plate would have looked like to the director on the shoot.

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/colourspace_nuke_setup.jpg" class = "responsive-image"/>

## Exporting from Nuke

For exporting you have a couple of options, and it really depends on project, most likely, you'll want to export as Raw, without any OCIO or LUTs baked in. This gives you the most flexibility for creating your delivery format

You can now convert these EXRs to:

- Create write into a viewing copy in Nuke
- Bring into Resolve, reverse the grade conversion and create our delivery format

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled%207.png" class = "responsive-image"/>

- To create a viewing copy, I have read in the EXR sequence, and cloned our *Linear → Plate Colourspace → Rec 709* LUT, and exported as RAW, you can do this with a png, jpg, tif or Mov etc

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled%208.png" class = "responsive-image"/>

---

## Delivering with Resolve

If we do want to deliver in the colourspace we recieved the plate in, we need to reverse the conversion we did initially, to do this, we must go back into Resolve. As you remember, we created a *Camera Colourspace → Linear*  now we msut do the opposite

- Import your Comped EXR Sequence, and create a Timeline with it
- In the colour tab, we want to create a *Linear → Camera Colourspace* LUT, this will convert the footage back into the flat Arri or sLOG look we imported.

<img src="/assets/post_images/Plate%20Processing%20Colourspace%20and%20OCIO/Untitled%209.png" class = "responsive-image"/>

Convert plate back to Flat look

You should now export your plate from Resolve in the delivery format, be that DNX or a TIF sequence

You can export the original colourspace from Nuke by exporting this *Linear → Camera Colourspace* LUT, but I have had problems with clamping on MOVs and TIFs, so you are limited to exporting flat EXRs, which then will need to be converted to a friendlier delivery format anyway (TIF or DNX Mov)