"use client";

import { ShaderAnimation } from "@/components/ui/shader-lines";

/**
 * Hero scoped atmospheric backdrop.
 * Three stacked layers:
 *   1. ShaderAnimation (mix-blend-screen, soft radial mask)
 *   2. Vignette · radial darken behind hero text for legibility
 *   3. Bottom fade · blends into page bg before next section
 * ShaderAnimation itself skips on mobile and reduced motion.
 */
export function ShaderBackdrop() {
  const shaderMask =
    "radial-gradient(ellipse 75% 60% at 50% 42%, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.7) 35%, rgba(0,0,0,0.35) 65%, rgba(0,0,0,0) 92%)";

  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 z-0 overflow-hidden"
    >
      {/* shader · z-base */}
      <div
        className="absolute inset-0 opacity-[0.45] mix-blend-screen"
        style={{ WebkitMaskImage: shaderMask, maskImage: shaderMask }}
      >
        <ShaderAnimation />
      </div>

      {/* vignette · darkens behind text zone */}
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse 60% 48% at 50% 50%, rgba(20,18,15,0.78) 0%, rgba(20,18,15,0.55) 28%, rgba(20,18,15,0.25) 55%, rgba(20,18,15,0) 80%)",
        }}
      />

      {/* bottom fade · blends shader edge into page bg */}
      <div
        className="absolute inset-x-0 bottom-0 h-40"
        style={{
          background:
            "linear-gradient(to bottom, rgba(34,31,27,0) 0%, var(--bg) 90%)",
        }}
      />
    </div>
  );
}
