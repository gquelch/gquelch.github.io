---
title: SPI-Anim in Nuke + Redshift
layout: post
published: true
---

# SPI-Anim

A step between standard sRGB workflow and ACES, this will not affect the amount of colour available, just the amount of lighting you can put in the scene, and the falloff. Overall the result will be darker than sRGB, so compensate by increasing the intensity of the lights

When we are working with SPI-Anim, we are actually still working on the same linear image as our standard Linear/sRGB workflow, we just have access to more range that is stored in the lighting, meaning we get a bit more flexibility to push our lighting

[Latest OCIO downloads](https://opencolorio.org/downloads.html)

## Redshift Setup

- Maya - Colour Management

We don't need to change anything in the Maya colour management settings to be able to use SPI-Anim

- Redshift Render View - Colour Management

We want to load our config into the Redshift render view, I usually disable this for file output, so that I am still outputting our standard EXR

<img src="/assets/post_images/SPI%20Anim%20in%20Nuke%20Redshift/RS_Config.png" class = "responsive-image"/>

Model kindly provided by [Chris Hunt](https://www.artstation.com/christopherhunt3d)

## Nuke 9 Setup

When setting up for Nuke we want to be sure to use the same configs, I always set it to custom, so I can be sure the version is the same between Redshift and Nuke

<img src="/assets/post_images/SPI%20Anim%20in%20Nuke%20Redshift/Nuke_Config.png" class = "responsive-image"/>

Because OCIO support in Nuke 9 was a bit more basic, we actually have to do a few more steps to get the image to display correctly.

- For Linear EXRs (our renders, for instance) they will display as expected in OCIO
- For PNGs, JPGs, TIFs, MOVs... anything we bring in that is in sRGB, we will need to convert manually, to do this, we need an "OCIO colourspace" node

<img src="/assets/post_images/SPI%20Anim%20in%20Nuke%20Redshift/Untitled.png" class = "responsive-image"/>

Here you can see I am using an OCIO colourspace in order to convert our sRGB PNG "*vd16*" to "*Inf*" This is the SPI-Anim version of converting from sRGB to Linear. I have set my Read node to use "raw data" so that we are totally in control of the conversion with the OCIO colourspace node.

This is the same for Exporting with OCIO

<img src="/assets/post_images/SPI%20Anim%20in%20Nuke%20Redshift/Untitled%201.png" class = "responsive-image"/>

Here I have set the Write node to use "raw data" and have set the "out" colourspace in our OCIO Colourspace node to use vd16, this will give us an image that will display properly outside of Nuke

### Examples

<img src="/assets/post_images/SPI%20Anim%20in%20Nuke%20Redshift/comparison.png" class = "responsive-image"/>

Model kindly provided by [Chris Hunt](https://www.artstation.com/christopherhunt3d)

Here is a quick comparison of the standard Linear/sRGB workflow vs using SPI-Anim. At first glance you'll notice we get a much more contrasty render. If you compare areas around the head, and characters right arm, you'll notice we have less peaking/over exposure, we actually have retained detail in these areas. SPI-Anim allows us to make more use of the range stored in an EXR file, so instead of values clipping at 1, we are able to use the data that goes above 1, which results in a farm more premium looking render. Because we have more range, we are able to actually boost the lights, so in turn we get more light bounce as well. The one side of it I dislike is the extra saturation, I feel it goes a little too far and usually end up reducing this in comp.

### Summary

OCIO gives us:

- Less over-exposure
- Stronger lights resulting in more bounce and GI
- More Contrast
- More saturation

Whilst having to change very little in our overall workflow, compared to something like ACES, which is a very different rendering space, and made tricky when working with Redshift, as it currently does not support the conversion.