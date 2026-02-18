# Portfolio Landing Page - Circular Spotlight Effect

Source: https://x.com/chddaniel/status/2019546310664417660

## Prompt

Create a personal portfolio landing page for [YOUR NAME] built as a single full-screen hero that occupies the entire viewport. Use a large portrait image [IMAGE ONE] as the background, centered and scaled to cover the screen. Place my name in the top-left corner in an elegant serif font such as Playfair Display, with a professional title directly beneath. In the bottom-right corner, add a minimal footer with social links (LinkedIn, GitHub, Twitter). All text should be rendered in a dark tone.

The signature interaction is a circular highlight (cursor) that follows the mouse smoothly with a slight delay. This circle reveals a second version of the portrait [IMAGE TWO] beneath the main image, like a cutout lens or portal. As the user moves the cursor, they see the alternate photo through the circle, while the rest of the background remains the default image. On fast movement, leave behind fading echoes (ghost circles) that quickly dissolve.

In the background behind everything, place a subtle animated grid pattern made of thin lines that slowly shift in perspective or gently pulse, adding depth without competing with the portraits.

When the circular highlight passes over the name or footer text, the text should dynamically invert to white for contrast against the revealed image.

Add a very slight parallax effect: the background portrait and the foreground text/grid should respond differently to mouse position, creating a feeling of layered depth.

The overall aesthetic should be minimal, refined, and moody. Use smooth transitions and spring-based or eased animations. No harsh edges, no loud colors. The design speaks through motion and contrast.

## Technical Notes
- Single full-screen hero (100vh)
- Two layered images (default + revealed via circular mask)
- Mouse-following circular reveal with spring-based easing
- Ghost/echo circles on fast movement
- Animated grid background (CSS or canvas)
- Text color inversion on highlight pass
- Parallax depth between layers
- Elegant serif font (Playfair Display or similar)
