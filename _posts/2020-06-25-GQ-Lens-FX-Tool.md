---
title: GQ Lens FX Tool
layout: post
published: true
---

This is my all in one tool for depth of field, it brings several popular depth of field nodes together into one gizmo. This allows you to swap between different tools on the fly, and adjust them all with a set of simple, real world controls.

The driving force behind this tool was to create digital "Lens Sets" as you would have on a Live Action shoot, it becomes simple to keep lens consistency across an entire project. You can customise each lenses focal length and optical qualities, some of which are tied to the aperture of the lens, the more you open the lens, the stronger the effects.

Supported Gizmos:

- ZDefocus
- pgBokeh
- OpticalZDefocus

One common problem with compositing depth of field is edge artefacts, sometimes switching tools is enough to solve it. The best way to get rid of the problem (without Deep) it is to separate out the comp into BG and FG layers and defocus them individually. This tool supports that workflow with a Master/Child relationship, you are able to duplicate the gizmo, and use the "Set Master" button to make that node control others. Child nodes will become locked, meaning you only have to tweak the master.

<img src="/assets/post_images/GQ%20Lens%20FX%20Tool/Untitled.png" class = "responsive-image"/>

Get the gizmo from [here](https://github.com/gquelch/Nuke-Public-Gizmos/blob/master/gizmos/LensFX_GQ_1.1.nk)

For specific details and demos on adding 3rd party gizmos, see the documentation [here](https://github.com/gquelch/Nuke-Public-Gizmos#lensfx_gq)