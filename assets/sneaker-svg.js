/* Sneaker silhouette SVG generator
   Renders a stylized low-top sneaker with configurable upper/sole/accent colors,
   model label, and colorway name. Used as placeholder until real photos arrive.
*/

function sneakerSVG({ upper = '#1a1a1a', sole = '#fff', accent = '#fa5400', laces = '#fff', modelLabel = '', colorwayName = '', bgGradient = true } = {}) {
  const bg1 = '#f5f5f5';
  const bg2 = '#e8e8e8';
  const bg = bgGradient
    ? `<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${bg1}"/><stop offset="1" stop-color="${bg2}"/></linearGradient></defs><rect width="600" height="600" fill="url(#bg)"/>`
    : `<rect width="600" height="600" fill="${bg1}"/>`;

  // Generic high-top silhouette (stylized, not any specific model)
  // Coordinates designed to fit 600x600 viewBox, shoe centered around y=360
  const shoe = `
    <g transform="translate(70,260)">
      <!-- sole -->
      <path d="M5,195 Q5,210 25,215 L445,215 Q465,210 465,195 L465,170 Q460,160 440,158 L30,158 Q10,160 5,170 Z"
            fill="${sole}" stroke="#000" stroke-width="2"/>
      <!-- midsole highlight -->
      <rect x="8" y="172" width="452" height="4" fill="${accent}" opacity="0.85"/>
      <!-- upper main -->
      <path d="M25,158 Q25,80 140,50 Q200,30 280,30 Q360,32 400,90 L440,120 Q460,140 458,158 Z"
            fill="${upper}" stroke="#000" stroke-width="2"/>
      <!-- toe box seam -->
      <path d="M70,158 Q80,100 160,75" stroke="${accent}" stroke-width="2.5" fill="none" opacity="0.9"/>
      <!-- swoosh-like sweep -->
      <path d="M140,130 Q220,90 360,130 Q380,138 375,155"
            stroke="${accent}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <!-- heel tab -->
      <path d="M390,80 Q420,65 440,95 L440,120 L400,115 Z" fill="${accent}" opacity="0.9"/>
      <!-- collar -->
      <path d="M220,30 Q250,15 300,22 Q340,30 355,50 Q330,45 290,45 Q245,45 225,55 Z"
            fill="${upper}" stroke="#000" stroke-width="1.5" opacity="0.92"/>
      <!-- laces -->
      <g stroke="${laces}" stroke-width="2.5" fill="none" opacity="0.85">
        <line x1="180" y1="85" x2="220" y2="78"/>
        <line x1="175" y1="105" x2="225" y2="98"/>
        <line x1="170" y1="125" x2="230" y2="118"/>
        <line x1="168" y1="145" x2="232" y2="138"/>
      </g>
      <!-- eyestay line -->
      <path d="M165,70 Q200,58 240,55" stroke="#000" stroke-width="1.5" fill="none" opacity="0.4"/>
    </g>
  `;

  const label = `
    <g font-family="Helvetica Neue, Arial, sans-serif" fill="#1a1a1a">
      <text x="40" y="70" font-size="13" font-weight="700" letter-spacing="3" fill="${accent}">${modelLabel.toUpperCase()}</text>
      <text x="40" y="110" font-size="30" font-weight="900" letter-spacing="-0.5">${colorwayName}</text>
      <text x="40" y="570" font-size="10" font-weight="600" letter-spacing="2" fill="#999">SNEAKERS.COLLECTION · PLACEHOLDER</text>
    </g>
  `;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">${bg}${shoe}${label}</svg>`;
}

// Export as data URI for inline use
function sneakerDataURI(opts) {
  const svg = sneakerSVG(opts);
  return 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
}

// Browser global + CommonJS
if (typeof window !== 'undefined') {
  window.sneakerSVG = sneakerSVG;
  window.sneakerDataURI = sneakerDataURI;
}
if (typeof module !== 'undefined') {
  module.exports = { sneakerSVG, sneakerDataURI };
}
