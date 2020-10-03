---
title: Plate Processing - Colourspace and OCIO - Part One
layout: post
published: false
---

When working on a VFX project it's important to keep consistent colour and quality of footage between software and throughout the pipeline. Some projects require delivery in a specific colourspace, maybe *Rec709*, whilst others need to be delivered in the colourspace they were provided in. We should have a clear understanding of how we are processing footage, and how to return to its original colourspace for delivery.

In part one I will be covering how I convert footage to linear before we bring it into Nuke, using Resolve. This process relies on having conversion LUTs (Look Up Tables) for that colourspace, *sLog2, sLog3,* *LogC,* *BMDFilm* are some examples. In part two I will be covering colourspaces such as *DLOG*, where we do not have a linear conversion LUT, therefore need ta different approach.

[DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve/) offers great visual control over colourspace, there are plenty of great resources for learning it online, so I won't go to in depth with how to use it, I learned a lot from [MiesnerMedia](https://www.youtube.com/channel/UC_4HXushRwS_9b1JdRFYVgw) and by experimenting with it.

This guide is **not applicable** for ACES, but will work with simpler OCIO configs such as [Filmic Blender](https://sobotka.github.io/filmic-blender/) and [SPI-Anim](https://github.com/imageworks/OpenColorIO-Configs/tree/master/spi-anim), as well as the standard Linear/sRGB workflow.

# Importing the Plate

Our first step is importing the footage. Bring the plate into Resolve Media Tab, you can simply drag the footage from the file explorer into the Media Pool. You'll probably get a pop-up asking you to change the project settings to match the clip you just added. I usually press yes, but will check the settings later.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled.png" class = "responsive-image"/>

### Timeline

There are several ways to create a timeline in Resolve, I often choose to right click on the footage and select "Create New Timeline Using Selected Clips..." 

We will be prompted to name it, I usually stick to a convention such as "PRJ\_seq#\_shot#\_" or "PRJ\_shot#\_" But name it whatever you feel is appropriate. I recommend creating one timeline per plate.

**It's important to add an underscore at the end**, this will separate our name from our frame padding when we export the footage.

We should now check our project and timeline settings are correct, we do this in "File" → "Project Settings". You want to check the frame rate, pixel aspect ratio and resolution are correct.

You can trim the clip on your new timeline using the Edit Tab.

## Linearizing the Plate

Footage should always be shot in a "flat" colour profile, where nothing is pure white or pure black. This gives you more flexibility when it comes to grading it.

As standard, we work in Linear colourspace, so the first thing we need to do is convert the plate from the flat colourspace to Linear. We do this in the Colour tab. 

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%201.png" class = "responsive-image"/>

Resolve has many built in LUTs for converting footage. Which one you use depends on the camera make and model the footage was shot with; Arri uses *LogC*, Sony uses *sLog2* or *sLog3*. You should be able to find this information online, from your footage metadata or, ideally, from the camera department responsible for the shoot. It's important you use the right one so the footage is Linearized correctly. Here is the plate I am using, its in *sLog2*:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%202.png" class = "responsive-image"/>

Resolve uses a node graph to manage colour grading, we can add a LUT to each node in the graph, by default you start out with one node. You can add more in sequence with ALT+S. We can pick the LUT for each node by right clicking on it, and opening to the LUTs menu.

The footage I have here was shot in *sLog2*, using the right click menu I have selected the *sLog2 → Linear* LUT*.* I'm not going to worry about over-exposure or balancing the plate, the point is to maintain exactly what we were given.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%203.png" class = "responsive-image"/>

Here is my plate linearized:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%204.png" class = "responsive-image"/>

## Exporting from Resolve

Now we want to export the plate, I usually do two exports, one for the Lighting and Compositing artists, as Linear EXRs, and a proxy export for the animators, as a Linear TIF sequence.

Linear TIFs will display incorrectly by default in most software, because it is assumed TIFs are already in *sRGB* space. However, this saves us from creating multiple timelines in Resolve, so if you need to adjust the edit you only need to change one timeline.

It's up to you if you export a proxy at this point. You will need to remove lens distortion from the animators image sequence. You can do this however you like, one option would be to load your EXR sequence into Nuke, undistort, down-res and write out as a TIF sequence. In this case you wouldn't need the TIF sequence from Resolve. It depends on how you or your studio deals with Lens Distortion.

Exporting from Resolve is done via the Delivery tab. The first is step is to set the folder destination of exports.

## EXR Export

### File Settings

- Enable "Timeline name" which keeps our export name consistent with our timeline name
- "Digits in the filename" is frame padding, 4 is usually plenty
- I usually enable "Each clip starts at frame" and set it to 1000
- You can use the "File Subfolder" to automatically put this export into a new folder, I usually name this the resolution of the footage, in this case 1080

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%205.png" class = "responsive-image"/>

### Video Settings

- Format EXR
- Codec *RGB Half* is usually plenty for camera footage. Check the specs of the camera to confirm this, if you are unsure, RGB half will likely be plenty
- Our resolution and frame rate should be correct based on our project settings
- Sometimes we may need to set our project to Cinemascope (2:1) aspect ratio, if this is an Anamorphic Project

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%206.png" class = "responsive-image"/>

You should now add this job to the queue

## TIF Proxy Export

You can keep the destination the same, so long as you are using the "File Subfolder" option, otherwise you need to change the location manually.

### File Settings

- For the TIF export we will be lowering the resolution, so we only need to change the "File Subfolder", in this case I will be rendering at 1280*720

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%207.png" class = "responsive-image"/>

### Video Settings

- For "Format" want to pick "RGB 8Bits LZW Compression". We can't write PNGs or JPGs out of resolve, so this is the best option that will keep the file size low
- Lower the resolution for faster playback

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%208.png" class = "responsive-image"/>

Now you can add this job to the queue, once you are happy you can select both jobs in the "Render Queue" and hit "Start Render". If you need to edit a job then use the pencil icon in the "Render Queue".

# Colour setup for Nuke

Although our footage was filmed in a flat colourspace, it will most likely have been viewed with a *Rec709* LUT. To see this we can create a separate node (not connected to your *Plate Colourspace → Linear* node) that uses the *Plate Colourspace → Rec709* LUT, like so:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%209.png" class = "responsive-image"/>

We want to view our footage and CG under this grade to be sure the comp will look good when it is graded by the client. If you bring your EXR sequence into Nuke, you'll notice it won't match. The specific colourspace and workflow you are using determines which steps you need to take next.

Depending on your workflow and colourspace, you have three options:

- **Work in Rec709** - *sLog2, sLog3*
- **Creating a Display LUT for Nuke** - *sLog2, sLog3, LogC, BMDFilm*
- **Creating a Display LUT for Nuke with OCIO** - Any workflow involving OCIO configs such as SPI-Anim should use this

### Work in Rec709

By default, Nuke, as well as many render engines such as Arnold, Renderman and Redshift are set to display in *sRGB*, whereas we want to display our footage in *Rec709*. You can change this in Nuke in the top menu above the viewer. With *sLog2* and *sLog3* footage you only need to change Nuke to display in *Rec709* for it to match Resolve. We don't need any additional LUTs for this workflow.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2010.png" class = "responsive-image"/>

Bear in mind that you will want your lighting artists Render Engine to also be set to *Rec709*, otherwise the gamma won't match between Maya and Nuke.

This is the workflow I would recommend for *sLog2* and *sLog3*, however you can use the next method if you do not want to switch to *Rec709*.

### Creating a Display LUT for Nuke

If you are using a LUT in resolve from the 3D LUT menu, such as Arri *LogC → Rec709* you will need to export it from Resolve to use in Nuke. This method will allow you to continue working in *sRGB* in Nuke, rather than changing to *Rec709*.

We need to create a LUT that converts from Linear, back to our plate colourspace and then to our final LUT, like so: *Linear → Plate Colourspace → Rec709.*

In order to make sure I'm doing this properly, I import the EXR sequence back into Resolve. Simply drag your 1080/EXR folder into the medial pool, right click it, and "Create New Timeline Using Selected Clips" I name this "PRJ\_NukeDisplayLUT". 

You can do this on the original timeline, however the image won't appear correctly in Resolve, because your original footage hasn't been linearized. The nodes you create however are the same, so once you export and load the LUT into Nuke, it will work.

We want to follow these steps to create the LUT:

- Using the right click menu, set the first node to *Linear → Plate Colourspace*
- Create a second node in sequence using ALT+S, on this node we want to convert from *Plate Colourspace → Rec709*

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2011.png" class = "responsive-image"/>

If you have the *Plate Colourspace → Rec709* LUT enabled on your original timeline, it should now match this new timeline.

We can export these nodes as a LUT by right clicking on the clip thumbnail in the timeline and selecting "Generate 3D LUT (65 Point Cube)". I name it to match the colour conversion I'm doing, here that would be: "*Linear\_sLog2\_Rec709"*

We can now load this LUT into Nuke and apply it with a "Vectorfield" as shown below. Remember that Nuke should be set to *sRGB* for this workflow.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2012.png" class = "responsive-image"/>

When using the Vectorfield, we need to make sure Colourspace In and Out are set correctly. Colourspace In should be set to that of our plate, in this case, we have converted it to Linear. Colourspace Out should match the display space of Nuke, in this case, we are using *sRGB*

This gives you two ways to view the footage, with and without the LUT. Both lighting and compositing artists will mainly work on the *sRGB* image, it will be the responsibility of your compositors to check the work still looks good with the LUT enabled.

### Creating a Display LUT for Nuke with OCIO

If we are using OCIO we need to take an additional step in Nuke to convert the colourspace properly.

Same as the Display LUT workflow above, compositing artists will have two ways to view the footage, the display transform of the OCIO config, and the LUT itself.

You want to create the same *Linear → Plate Colourspace → Rec709* LUT I have outlined above and export it from Resolve the same way:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2011.png" class = "responsive-image"/>

Again we are applying this with a Vectorfield, but we want to keep both the Colourspace In and Out set to Linear.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2013.png" class = "responsive-image"/>

Usually we would expect to use *sRGB* or *Rec709* as the colourspace Out, however our OCIO config will have a custom colourspace LUTs that it uses to convert *sRGB* or *Rec709* footage. In the case of SPI-Anim, *vd16* is what we use to process *sRGB* images, so we want to convert from *vd16 → Linear.*

Unfortunately the Vectorfield won't recognise we are using OCIO. So to use an "OCIOColorspace" node, like so:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2014.png" class = "responsive-image"/>

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2015.png" class = "responsive-image"/>

The OCIOColorspace is now taking care of the final part of the conversion, and should match the Resolve viewer.

# Maya Setup

Before I talk about how we export from Nuke, I will show you the plate setup in Maya.

## Lighting

Using Redshift, we can see our plate in the render view by using the Back-Plate function on a DomeLight. This will allow us to see our CG on top of the plate, making the lighting process more interactive. Because we are using Linear EXRs the plate will display correctly, there is an "sRGB" button if you want to use an *sRGB* sequence.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2016.png" class = "responsive-image"/>

Redshift Dome Light

Using Arnold you need to load the image in as a "BG Image" in the Arnold render view.

Both renders will let you pick between colourspaces using their render view, including *sRGB* and *Rec709*. 

For OCIO in Redshift, you load the config directly into the Render View. In Arnold, you need to add it to Maya's Colour management settings for the display LUTs to appear in the render view menu.

## Animation

We need to give the animators the plate without Lens Distortion, as I discussed when exporting the plate from Resolve. This means we can apply the distortion directly to the CG without changing the plate, ensuring its quality remains high.

Once you have an undistorted sequence, you simply load it in as an "Image Plane" on the camera, if you are using the Linear TIF sequence, you want to set the colourspace to *Raw*

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2017.png" class = "responsive-image"/>

Image Plane

## Exporting from Nuke

When it comes to exporting your comp there are a couple of options, and it depends on the project. Most likely, you'll want to export Linear EXRs, without any OCIO or LUTs baked in first. This gives you the most flexibility when creating your delivery format.

You can then use those EXRs to:

- Create a viewing copy (MOV/MP4) in Nuke
- Bring into Resolve, return the comp to the original LUT, and create a delivery format

## Rec709 Workflow

For *Rec709* exporting is simple, as we have no extra viewer LUT! You just want to make sure the Write node is exporting Linear EXRs. I have included a comparison between the software displays and renders, so you can see the consistency.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2018.png" class = "responsive-image"/>

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/rec709_comparison.png" class = "responsive-image"/>

## LUT Workflow

With the LUT workflow, we want to be careful **not to export the Vectorfield**. This will avoid any extra work in Resolve, I usually set it up like so:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2019.png" class = "responsive-image"/>

I haven't included a comparison here, as the difference between the *sRGB* display LUT space and *Rec709* LUT from Resolve is very subtle. See the OCIO comparison for an example.

## OCIO Workflow

For OCIO the setup is almost the same, except for the additional OCIO Colourspace node. We do not want to export the Viewing LUT.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2020.png" class = "responsive-image"/>

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/OCIO_comparison.png" class = "responsive-image"/>

What you'll notice is the top row all match the Resolve Display, the bottom row all match each other, but they **do not** match Resolve. This is correct, as we are viewing with the Film(sRGB) display LUT from SPI-Anim. 

Notice how we have less peaking in the clouds and on top of the sphere, we can see the spec reflection on the sphere now as the LUT has reduced highlight clamping, we also have slightly deeper blacks. The lighting and comp artists should work using the same display LUT, however the compositors should also check the work with the *Rec709* LUT, to make sure work looks good with it. 

If you were to export the SPI-Anim and *Rec709* renders as Linear, with no LUTs baked in, bring them back into Resolve and convert them both to *Rec709*, they will be the same. With both workflows we are working on the same Linear image, we are just displaying them differently. SPI-Anim will allow your lighting artists to push the lighting more, and get a better result.

## Viewing Copy from Nuke

Once we have rendered the comped EXR sequence, you can read it back in, clone the Viewing LUT nodes (Vectorfield and OCIO colourspace if you have it), and then write out to the format you need (png, jpg, tif, Mov etc) to make a viewing copy, you should set the Write node to *sRGB* for this.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2021.png" class = "responsive-image"/>

## Delivering with Resolve

If we want to deliver in the colourspace we received the plate in, we need to reverse the conversion we did initially, to do this, we must bring our comped EXR sequence into Resolve. 

The first step in converting the plate was to create a *Camera Colourspace → Linear* node, now we do the opposite. With all three methods above, this step will be the same - so long as you have exported the Linear EXRs with no LUTs from Nuke.

- Import your Comped EXR Sequence to Resolve, and create a Timeline from it
- In the Colour tab, we want to use a *Linear → Camera Colourspace* LUT, this will convert the footage back to its original colourspace.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/Untitled%2022.png" class = "responsive-image"/>

You can export the *Linear → Camera Colourspace* LUT and use it in Nuke to return to your flat colourspace, but I have had problems with clamping on MOVs and TIFs, meaning you are limited to exporting flat EXRs. These then need to be converted to a better delivery format anyway, likely TIF or MOV. So in the end I found using Nuke takes longer for this.

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20One/resolve_comparison.png" class = "responsive-image"/>

I hope the guide has been helpful, colourspace is a complicated topic with lots of variables, but I have provided some options and solutions. Following this you should be able to maintain consistency throughout the workflow. We can then to return the plate to the original LUT. This means the client can do an initial grade on the footage before the CG is finished, and easily swap out the plate with the comped sequences before the final grade.