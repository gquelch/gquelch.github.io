---
title: Colour Checker Nuke Workflow
layout: post
published: true
---

Get the tool from [Here](https://github.com/gquelch/Nuke-Public-Gizmos)

There are a lot of automated tools out there for using a macbeth chart in Nuke, such as [mmColorTarget](http://www.nukepedia.com/gizmos/colour/mmcolortarget), but sometimes you want to have manual control over what is happening, for instance MM_ColourTarget will output a colour matrix, which is very hard to tweak if you want to use this to grade your CG element. 

With this workflow you can simply copy the grade nodes over to your CG elements and use them as a starting point for the grade.

First step is to set position of Reference colour checker. You want to position all 4 points on the corners of your checker

<img src="/assets/post_images/Colour%20Checker%20Nuke%20Workflow/Untitled.png" class = "responsive-image"/>

Then you want to do the same process for your Render checker

<img src="/assets/post_images/Colour%20Checker%20Nuke%20Workflow/Untitled%201.png" class = "responsive-image"/>

You now have 3 options for displaying your colour checkers

- Merged

    This places your Render checker on top of the Reference checker in the plate, good for checking the colours in situ

    "Disable Masking" will switch this display to view the full Render checker, without masking, on top of the plate

- Ref / Render

    This will be a full screen display of your Reference, on top of your Render. Viewing the Alpha channel of this output will display the Saturation values of your checkers.

- Render / Ref

    This will be a full screen display of your Render on top of your Reference. Viewing the Alpha channel of this output will display the Saturation values of your checkers.

You can now start using colour nodes to adjust the value and saturation of your Render checker in order to match it to your reference, check the saturation by viewing the Alpha channel.

I will go through channel by channel (R G B A(saturation when using this node) Y) and make small adjustments to start aligning the colours.

You can spend as much time as you like tweaking the values to get a match for your plate, I often get something that is quite close but I will be using these grades just as a base, and will be tweaking them more artistically later, so it does not need to be perfect.

Here is a rough match up for my checkers, viewed with *Render / Ref*, you would spend more time doing this with a real Render, I have just done this for demonstration purposes

<img src="/assets/post_images/Colour%20Checker%20Nuke%20Workflow/Untitled%202.png" class = "responsive-image"/>

I can now take these grade nodes and copy them to my CG Render, and in theory, we have a starting point for our comp with nicely matched colours to our plate. In an ideal workflow, with a good HDR and Reference Colour Checker, you shouldn't need to do much to your Render Colour Checker in order for it to match, the closer they match without having to grade, the better job you have done at re-creating the real world lighting.