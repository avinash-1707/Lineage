import type { CSSProperties } from "react";

const COLS = 4;
const ROWS_PER_TILE = 26;
const CELL = 28;

function buildTile(seed: number) {
  let s = seed >>> 0;
  const rand = () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 0x100000000;
  };

  const rects: string[] = [];
  for (let r = 0; r < ROWS_PER_TILE; r++) {
    for (let c = 0; c < COLS; c++) {
      const v = rand();
      if (v < 0.018) {
        rects.push(
          `<rect x='${c * CELL + 2}' y='${r * CELL + 2}' width='${CELL - 4}' height='${CELL - 4}' fill='%237a8aa6' fill-opacity='0.62'/>`
        );
      } else if (v < 0.028) {
        rects.push(
          `<rect x='${c * CELL + 2}' y='${r * CELL + 2}' width='${CELL - 4}' height='${CELL - 4}' fill='%235a6c8a' fill-opacity='0.34'/>`
        );
      } else if (v < 0.034) {
        rects.push(
          `<rect x='${c * CELL + 9}' y='${r * CELL + 9}' width='${CELL - 18}' height='${CELL - 18}' fill='%237a8aa6' fill-opacity='0.85'/>`
        );
      }
    }
  }

  const w = COLS * CELL;
  const h = ROWS_PER_TILE * CELL;
  return `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='${w}' height='${h}' shape-rendering='crispEdges'>${rects.join("")}</svg>")`;
}

const LEFT_TILE = buildTile(0x9e3779b1);
const RIGHT_TILE = buildTile(0x85ebca6b);

const LINE_COLOR = "rgba(205, 195, 168, 0.07)";

const gridLines =
  `linear-gradient(to right, transparent calc(${CELL}px - 1px), ${LINE_COLOR} calc(${CELL}px - 1px), ${LINE_COLOR} ${CELL}px), ` +
  `linear-gradient(to bottom, transparent calc(${CELL}px - 1px), ${LINE_COLOR} calc(${CELL}px - 1px), ${LINE_COLOR} ${CELL}px)`;

const baseSize = `${COLS * CELL}px ${ROWS_PER_TILE * CELL}px, ${CELL}px ${CELL}px, ${CELL}px ${CELL}px`;
const baseRepeat = "repeat-y, repeat, repeat";

const fadeY = "linear-gradient(to bottom, transparent 0%, black 4%, black 96%, transparent 100%)";

const fadeXLeft =
  "linear-gradient(to right, " +
  "black 0%, rgba(0,0,0,0.96) 22%, rgba(0,0,0,0.78) 42%, rgba(0,0,0,0.52) 62%, rgba(0,0,0,0.22) 84%, transparent 100%)";

const fadeXRight =
  "linear-gradient(to left, " +
  "black 0%, rgba(0,0,0,0.96) 22%, rgba(0,0,0,0.78) 42%, rgba(0,0,0,0.52) 62%, rgba(0,0,0,0.22) 84%, transparent 100%)";

const wrapperLeftStyle: CSSProperties = {
  WebkitMaskImage: fadeY,
  maskImage: fadeY,
};

const wrapperRightStyle: CSSProperties = wrapperLeftStyle;

const leftStyle: CSSProperties = {
  backgroundImage: `${LEFT_TILE}, ${gridLines}`,
  backgroundSize: baseSize,
  backgroundRepeat: baseRepeat,
  backgroundPosition: "left top, left top, left top",
  WebkitMaskImage: fadeXLeft,
  maskImage: fadeXLeft,
};

const rightStyle: CSSProperties = {
  backgroundImage: `${RIGHT_TILE}, ${gridLines}`,
  backgroundSize: baseSize,
  backgroundRepeat: baseRepeat,
  backgroundPosition: "right top, right top, right top",
  WebkitMaskImage: fadeXRight,
  maskImage: fadeXRight,
};

export function SideGrid() {
  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 z-0 hidden overflow-hidden md:block"
    >
      <div
        className="absolute inset-y-0 left-0 w-[clamp(140px,calc((100vw-980px)/2),240px)]"
        style={wrapperLeftStyle}
      >
        <div className="absolute inset-0" style={leftStyle} />
      </div>
      <div
        className="absolute inset-y-0 right-0 w-[clamp(140px,calc((100vw-980px)/2),240px)]"
        style={wrapperRightStyle}
      >
        <div className="absolute inset-0" style={rightStyle} />
      </div>
    </div>
  );
}
