let model;
let isModelLoaded = false;

async function loadModel() {
    model = await tf.loadLayersModel('/static/model/model.json');
    console.log("Model loaded successfully!");
    isModelLoaded = true;
}

loadModel();

console.log("Gesture detector loaded.");

// === Stabilization Variables ===
let lastGesture = "none";
let gestureCount = 0;
const GESTURE_STABLE_FRAMES = 5;

let lastTriggerTime = 0;
const TRIGGER_COOLDOWN = 1200;

// === Swipe Variables ===
let lastX = null;
let lastY = null;
let swipeCooldown = 0;
const SWIPE_THRESHOLD = 0.13;
const SWIPE_COOLDOWN_MS = 900;

// === Canvas Setup ===
const video = document.getElementById("camera");
const canvas = document.getElementById("hand-canvas");
const ctx = canvas.getContext("2d");
canvas.width = 640;
canvas.height = 480;

function onResults(results) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (!results.multiHandLandmarks) return;

  for (const landmarks of results.multiHandLandmarks) {
    drawConnectors(ctx, landmarks, HAND_CONNECTIONS, { color:"#00FFAA", lineWidth:3 });
    drawLandmarks(ctx, landmarks, { color:"#FF0066", lineWidth:2 });

    // Swipe Detection
    const swipe = detectSwipe(landmarks);
    if (swipe) {
      showGestureOverlay(swipe);
      handleGesture(swipe);
      continue;
    }

    const gesture = classifyGesture(landmarks);

    if (gesture === lastGesture) gestureCount++;
    else {
      gestureCount = 0;
      lastGesture = gesture;
    }

    if (gestureCount === GESTURE_STABLE_FRAMES) {
      const now = Date.now();
      if (now - lastTriggerTime > TRIGGER_COOLDOWN) {
        lastTriggerTime = now;

        // === ML Prediction Layer ===
        if (isModelLoaded) {
          let img = tf.browser.fromPixels(video)
            .resizeNearestNeighbor([224, 224])
            .toFloat()
            .div(255.0)
            .expandDims();

          let prediction = model.predict(img);
          let index = prediction.argMax(1).dataSync()[0];

          console.log("ML Model Prediction:", index);
        }

        console.log("✔ Stabilized:", gesture);
        showGestureOverlay(gesture);
        handleGesture(gesture);
      }
    }
  }
}

// === MediaPipe Setup ===
const hands = new Hands({
  locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
});

hands.setOptions({
  maxNumHands: 1,
  modelComplexity: 1,
  minDetectionConfidence: 0.7,
  minTrackingConfidence: 0.5,
});

hands.onResults(onResults);

new Camera(video, {
  onFrame: async () => await hands.send({ image: video }),
  width: 640,
  height: 480
}).start();


// =======================================================
// === IMPROVED THUMB GESTURE DETECTOR (SUPER ACCURATE) ===
// =======================================================
function detectThumbGesture(landmarks) {
  const wrist = landmarks[0];
  const thumbCMC = landmarks[1];
  const thumbMCP = landmarks[2];
  const thumbIP  = landmarks[3];
  const thumbTIP = landmarks[4];

  // Thumb extended upward (vertical chain decreasing)
  const thumbExtended = 
      thumbTIP.y < thumbIP.y &&
      thumbIP.y < thumbMCP.y &&
      thumbMCP.y < thumbCMC.y;

  // Folded fingers check (allows slight raise)
  const indexFold  = landmarks[8].y  > landmarks[6].y  + 0.01;
  const middleFold = landmarks[12].y > landmarks[10].y + 0.01;
  const ringFold   = landmarks[16].y > landmarks[14].y + 0.01;
  const pinkyFold  = landmarks[20].y > landmarks[18].y + 0.01;

  const allFolded = indexFold && middleFold && ringFold && pinkyFold;

  if (!thumbExtended || !allFolded) return null;

  // Check vertical orientation relative to wrist
  const dy = thumbTIP.y - wrist.y;

  if (dy < -0.10) return "thumbs_up";
  if (dy >  0.10) return "thumbs_down";

  return null;
}


// =======================================================
// === CLASSIFY GESTURES ===
// =======================================================
function classifyGesture(landmarks) {
  function isFingerUp(tip, pip) {
    return tip.y < pip.y - 0.03;
  }

  const thumbTip = landmarks[4];
  const indexTip = landmarks[8];
  const indexPIP = landmarks[6];
  const middleTip = landmarks[12];
  const middlePIP = landmarks[10];
  const ringTip = landmarks[16];
  const ringPIP = landmarks[14];
  const pinkyTip = landmarks[20];
  const pinkyPIP = landmarks[18];

  const indexUp = isFingerUp(indexTip, indexPIP);
  const middleUp = isFingerUp(middleTip, middlePIP);
  const ringUp = isFingerUp(ringTip, ringPIP);
  const pinkyUp = isFingerUp(pinkyTip, pinkyPIP);

  // ---- Try improved thumb detection FIRST ----
  const thumbGesture = detectThumbGesture(landmarks);
  if (thumbGesture) return thumbGesture;

  // Palm
  if (indexUp && middleUp && ringUp && pinkyUp) return "palm";

  // Fist
  if (!indexUp && !middleUp && !ringUp && !pinkyUp) return "fist";

  // Index pointing
  if (indexUp && !middleUp && !ringUp && !pinkyUp) return "index";

  // Two-finger gesture
  if (indexUp && middleUp && !ringUp && !pinkyUp) return "two_fingers";

  // OK / Mute gesture
  const d = Math.hypot(thumbTip.x - indexTip.x, thumbTip.y - indexTip.y);
  if (d < 0.04) return "mute";

  return "unknown";
}


// =======================================================
// === SWIPE DETECTION ===
// =======================================================
function detectSwipe(landmarks) {
  const wrist = landmarks[0];
  if (swipeCooldown > Date.now()) return null;

  if (lastX === null) {
    lastX = wrist.x;
    lastY = wrist.y;
    return null;
  }

  const dx = wrist.x - lastX;
  const dy = wrist.y - lastY;

  lastX = wrist.x;
  lastY = wrist.y;

  if (dx > SWIPE_THRESHOLD) { swipeCooldown = Date.now()+SWIPE_COOLDOWN_MS; return "swipe_right"; }
  if (dx < -SWIPE_THRESHOLD){ swipeCooldown = Date.now()+SWIPE_COOLDOWN_MS; return "swipe_left"; }
  if (dy < -SWIPE_THRESHOLD){ swipeCooldown = Date.now()+SWIPE_COOLDOWN_MS; return "swipe_up"; }
  if (dy > SWIPE_THRESHOLD) { swipeCooldown = Date.now()+SWIPE_COOLDOWN_MS; return "swipe_down"; }

  return null;
}
