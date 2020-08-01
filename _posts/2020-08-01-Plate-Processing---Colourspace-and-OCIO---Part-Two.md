---
title: Plate Processing - Colourspace and OCIO - Part Two
layout: post
published: true
---

When working on a VFX project it's important to keep consistent colour and quality of footage between software and throughout the pipeline. Some projects require delivery in a specific colourspace, maybe *Rec709*, whilst others need to be delivered in the colourspace they were provided in. We should have a clear understanding of how we are processing footage, and how to return to its original colourspace for delivery.

In part one I covered linearizing footage using Resolve, in part two I will be covering how I convert footage to Linear using Nuke, without doing colour management in Resolve. This is useful when we need to use a Custom LUT (Look Up Table), with footage such as *DLOG*. I would recommend reading part 1 which includes more information about Resolve and the Maya setup.

Usually camera manufacturers provide a *Plate Colourspace → Linear* LUT. Sometimes this isn't the case, meaning we have to find another way to convert our footage. The ideal solution is to find the LUT online, or we find the expression for that colour conversion. Failing this, we can actually borrow a similar LUT to get the job done, but this is not as accurate, more of a last resort plan.

This guide is **not applicable** for ACES, but will work with simpler OCIO configs such as [Filmic Blender](https://sobotka.github.io/filmic-blender/) and [SPI-Anim](https://github.com/imageworks/OpenColorIO-Configs/tree/master/spi-anim), as well as the standard Linear/sRGB workflow.

I will be using *DLOG* footage as an example, from a DJI drone. Resolve comes with these LUTs for *DLOG*:

- *DLOG → sRGB*
- *DLOG → Rec709*
- *Linear → DLOG*

As you can see, DJI don't provide the *DLOG → Linear* LUT, so I have created this workflow to get around that.

For reference, this is the plate I am using, in *DLOG:*

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20Two/Untitled.png" class = "responsive-image"/>

We are still starting out in Resolve because the footage will need to be converted from a MOV format to an EXR sequence. We aren't going to apply LUTs here, instead the conversion will be done with Nuke. Once you've done this bring the EXR sequence into Nuke. It will be assigned the Linear conversion, so the footage will look more washed out than in Resolve. Don't worry as we will be creating the correct colour conversion LUT next.

# Finding the LUT or Expression

This is where I spent most time for this guide, DJI provide some LUTs [here](https://www.dji.com/uk/downloads/softwares/transcoding-zenmuse-x7-linear), but not what we need. [This topic](https://community.foundry.com/discuss/topic/136535/dji-d-log-linearization-lut?mode=Post&postID=1105856) on The Foundry forums touches on the issue, but doesn't provide a specific fix for *DLOG*.

It wasn't until I searched "DLOG Curve" that lead me to [this paper](https://www.heliguy.com/downloads/1527849526D-Log_D-Gamut_Whitepaper.pdf) which contains the information we need to convert *DLOG* footage **to and from Linear.** It also contains information about converting D-Gamut, but I won't be using that here - if you do need it, you want to take the values from the tables, and apply it to a 3x3 Colour Matrix in Nuke.

These are the expressions the paper gives us:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20Two/Untitled%201.png" class = "responsive-image"/>

Looks quite intimidating, but I will walk you through the steps to get this working in Nuke. You should note that "in" and "x" both refer to the value of a pixel.

If you are unable to find the expression you need, you may need to resort to using a different LUT that gives similar results, such as sLog2 or sLog3. In that case you can skip ahead and read "Using a different Conversion LUT" section below.

### DLOG → Linear

We use this equation to convert *DLOG* footage to a linear image we can work with for our CG. It a bit of tweaking first.

First off we are taking the "in" value, to see if it is less than or equal to (<=) 0.14

If it is, then we perform the first expression:

```
( x -0.0929 ) / 6.025
```

Then we are checking if that value is greater than (>) 0.14

If it is, then we perform the second expression:

```
( 10 ^ ( 3.89616 * x -2.27752 ) -0.0108 ) / 0.9892
```

 "^" means to the power of, usually expressed as:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20Two/Untitled%202.png" class = "responsive-image"/>

Nuke doesn't recognise this symbol, and instead uses:

```
pow (x, y)
```

Bearing that in mind, Nuke requires the expression to be written like so:

```
( pow ( 10 , ( 3.89616 * x - 2.27752 ) ) -0.0108 ) / 0.9892
```

So, we can simplify our greater and less than statements down to an if statement, with two outcomes:

```
if x <= 0.14:
	perform expression one

else:
	perform expression two
```

Nuke's expression node follows this format for if statements:

```
if this ? do this : else this
```

We first substitute in the if statement we are going to check:

```
x <= 0.14 ? perform expression one : perform expression two
```

Now we substitute in both expressions:

```
x <= 0.14 ? (x - 0.0929) / 6.025 : ( pow ( 10 , (3.89616* x -2.27752) ) -0.0108 ) / 0.9892
```

Next we take that expression and add it to each channel of an expression node:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20Two/Untitled%203.png" class = "responsive-image"/>

**Notice** I have **swapped "In" and "x" for r, g and b**, so we are adjusting each channel individually with the same expression.

Attaching this to our Read node will linearize the footage, here is my plate before and after the expression:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20Two/nuke_expression_comparison.png" class = "responsive-image"/>

### Linear → DLOG

We also need to be able to reverse this to return to our original flat colourspace. 

Applying the same principles to the other expression, we come out with this:

```
in <= 0.0078 ? 6.025 * in + 0.0929 : ( log10 ( in * 0.9892 + 0.0108 ) ) * 0.256663 + 0.584555
```

Put onto another expression node, again, swapping the in for r, g and b in their respective expressions:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20Two/Untitled%204.png" class = "responsive-image"/>

Upon connecting this to the first expression node, you should see the image return to its original state - Hooray!

## Setup as a Nuke LUT

This method is good, it's easy to share these two nodes, and you can put your *DLOG → Linear* node after any footage Read nodes, and *Linear → DLOG* before any write nodes, and export using "Raw Data"

But if you wanted to be cleaner, you can modify the expression slightly and add it to the Nuke Colour options in the Project Settings. This way it will appear in the Colourspace drop-down on the Read and Write nodes

You want to take the *DLOG → Linear* expression, and swap out the colour channel (r, g or b) for x, so the expression becomes:

```
x <= 0.14 ? ( x - 0.0929 ) / 6.025 : ( pow (10 , ( 3.89616* x -2.27752 ) ) -0.0108 ) / 0.9892
```

Then follow these steps:

- Hit "S" to open project settings
- Go to the "Color" Tab
- Below the list of colourspace LUTs you should see a "+", "Reset" and "-" button

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20Two/Untitled%205.png" class = "responsive-image"/>

- Using "+" you want to add and name your new LUT, I have simply called it DLOG
- Right click in the graph area of this LUT, and go to "Edit" → "Edit Expression"
- Paste the expression here.
- You should now be able to select this new cure in your Read and Write colourspace dropdown menus (you might need to remake the nodes for this to take effect)

# Using a different Conversion LUT

If you are unable to get the LUT you need for your footage, but do have the correct *Camera Colourspace → Rec709* LUT, you may get away with using a stand in LUT to do the conversion in Nuke. Specifically for the *DLOG* footage, I found *sLog3* gave me a similar result. Alternatively, if you're using [SPI-Anim](https://github.com/imageworks/OpenColorIO-Configs/tree/master/spi-anim) you could use *compositing_log* which also gives similar results. This won't correctly linearize the footage, however a *Camera Colourspace → Rec709* LUT will display correctly.

Technically, you can get away with using many of the Nuke LUTs, such as *sLog2*, *logC* or *compositing\_log*. You just need to make sure you set the "Colourspace In" on the vectorfield to match the LUT you have chosen. This ensures the footage is being returned to its original state, meaning the LUT will display correctly. I will explain the Vectorfield setup below.

## Comping and Matching Resolve

From here you can start compositing like usual. I would recommend you work in *Rec709* display space as that's what we're converting to, same goes for the Lighting Artists. Now you have converted the plate you can do exports with the LUT enabled for your animators, and export a Linear sequence for Lighting. When you come to do a final export, you simply set the Write node to *DLOG* to return to the original.

I would recommend you export the *Camera Colourspace → Rec709* LUT from Resolve, this way you can check your work closer to what the client will have seen on the shoot. I will use the *DLOG → Rec709* LUT, but you may be supplied with a specific one by the client.

You can load that onto a Vectorfield node like so:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20Two/Untitled%206.png" class = "responsive-image"/>

When using the Vectorfield, we need to make sure Colourspace In and Out are set correctly. You want to set In to the colourspace of our plate. We can use our *DLOG* LUT here. Set Out to match the display space of Nuke, in this case, we are using *Rec709*.

From here we can work and export as we like, I would recommend writing flat EXRs out of Nuke, from these files you can create a mp4 with the LUT baked, or take the footage back into Resolve to create a delivery format.

## OCIO and SPI-Anim

If you are using an OCIO plugin like SPI-Anim you will need to work slightly differently. Because the plugin overrides our default Nuke LUTs we have to use the expression nodes we created above.

Here are the things you will need to bear in mind:

- Final Write nodes should be set to "RAW"
- Plate Read nodes should be set to "RAW"
- We should be using the Expression nodes created above to do the plate conversions manually
- Our Viewing LUT will need to be converted back to *DLOG* before we apply the Vectorfield, and from sRGB (using *vd16* in SPI-Anim) back to Linear

Following all these steps will allow you to work in your OCIO config and still have a Viewing LUT that matches with Resolve. We are using the same principles of the standard workflow, however the conversions have to be done manually with additional nodes. Here is an example this setup:

<img src="/assets/post_images/Plate%20Processing%20-%20Colourspace%20and%20OCIO%20-%20Part%20Two/Untitled%207.png" class = "responsive-image"/>

## Closing Thoughts

This process was more complicated than I had anticipated when I began writing this guide. I hope I have broken down the workflow enough to make it easy to follow, to summarise:

- Find the LUT or expression curve online
- Adapt it to work with the Nuke Expression node
- Add it to the Nuke LUTs menu - optional but cleaner
- Export your LUT from Resolve to check your work with the correct grade
- When using OCIO do manual colour conversion with Expression nodes, and enable the "RAW" option on Read and Write nodes