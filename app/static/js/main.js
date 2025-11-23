// Ship Maintenance Tracker - Main JavaScript

// Placeholder for future client-side functionality
// Currently all interactive features are handled inline in templates

console.log('Ship Maintenance Tracker loaded');


// OBNOXIOUS ZOA ENERGY AD ROTATOR
const zoaMessages = [
    "⚓ Fuel your watch with ZOA Energy",
    "🚢 Power through your shift. Zero sugar. All energy.",
    "🔧 Keep the engines running. Keep yourself running.",
    "⚡ 160mg caffeine + vitamins for long voyages",
    "🌊 Stay alert on the open ocean with ZOA",
    "🛠️ Maintenance runs on caffeine. We've got you covered.",
    "🚢 The Rock's energy drink. Chief Engineer approved.",
    "⚓ Night watch? ZOA's got you. 24/7 energy.",
    "🔥 Zero sugar crash. Maximum maritime performance.",
    "⚡ Better ingredients. Better energy. Better watch.",
    "🚢 Trusted by engineers. Powered by ZOA.",
    "🌊 Navigate the seas. Navigate your day with ZOA."
];

const zoaVariants = ['', 'red-variant', 'purple-variant', 'orange-variant'];

function rotateZoaAd() {
    const messageEl = document.getElementById('zoa-message');
    const bannerEl = document.querySelector('.zoa-ad-banner');
    
    if (!messageEl || !bannerEl) return;
    
    // Random message
    const message = zoaMessages[Math.floor(Math.random() * zoaMessages.length)];
    messageEl.textContent = message;
    
    // Random color variant
    const variant = zoaVariants[Math.floor(Math.random() * zoaVariants.length)];
    bannerEl.className = 'zoa-ad-banner ' + variant;
}

// Rotate every 4 seconds (very aggressive)
if (document.querySelector('.zoa-ad-banner')) {
    rotateZoaAd();
    setInterval(rotateZoaAd, 4000);
}
