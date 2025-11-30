// ------------------- Song List -------------------
const songs = [
  { name: "A Christmas Tale", artist: "John Smith", file: "https://dhruv-1710.github.io/my-music-files/a-christmas-tale-263868.mp3" },
  { name: "Alone", artist: "Emily Rose", file: "https://dhruv-1710.github.io/my-music-files/alone-296348.mp3" },
  { name: "Bill Conti - The Final Bell", artist: "Bill Conti", file: "https://dhruv-1710.github.io/my-music-files/bill-conti-the-final-bell-rocky-128-ytshorts.savetube.me.mp3" },
  { name: "Cinematic Fairy Tale", artist: "Anna Melody", file: "https://dhruv-1710.github.io/my-music-files/cinematic-fairy-tale-story-main-8697.mp3" },
  { name: "In The Forest", artist: "Forest Sounds", file: "https://dhruv-1710.github.io/my-music-files/in-the-forest-ambient-acoustic-guitar-instrumental-background-music-for-videos-5718.mp3" }
];

// ------------------- DOM Elements -------------------
const songsListDiv = document.getElementById('songs-list');
const audio = new Audio();
const playBtn = document.getElementById('play');
const playBtn2 = document.getElementById('play2');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');
const prevBtn2 = document.getElementById('prev2');
const nextBtn2 = document.getElementById('next2');
const progressBar = document.getElementById('progress-bar');
const nowPlayingName = document.getElementById('now-playing-name');
const nowPlayingArtist = document.getElementById('now-playing-artist');
const currentTimeEl = document.getElementById('current-time');
const durationEl = document.getElementById('duration');

let currentIndex = 0;

// ------------------- Build Playlist -------------------
songs.forEach((song, i) => {
  const div = document.createElement('div');
  div.classList.add('song');
  if(i===0) div.classList.add('active');
  div.innerHTML = `<span>${song.name}</span><span>▶️</span>`;
  div.addEventListener('click', () => loadSong(i));
  songsListDiv.appendChild(div);
});

// ------------------- Update Now Playing -------------------
function updateNowPlaying(){
  nowPlayingName.innerHTML = `<span class="marquee">${songs[currentIndex].name}</span>`;
  nowPlayingArtist.textContent = songs[currentIndex].artist;
  document.querySelectorAll('.song').forEach((s,i)=> s.classList.toggle('active', i===currentIndex));
}

// ------------------- Load Song -------------------
function loadSong(index){
  currentIndex = index;
  audio.src = songs[currentIndex].file;
  audio.play();
  playBtn.textContent = '⏸️';
  playBtn2.textContent = '⏸️';
  updateNowPlaying();
}

// ------------------- Play/Pause -------------------
function togglePlay(){
  if(audio.paused){
    audio.play();
    playBtn.textContent='⏸️';
    playBtn2.textContent='⏸️';
  } else {
    audio.pause();
    playBtn.textContent='▶️';
    playBtn2.textContent='▶️';
  }
}
playBtn.addEventListener('click', togglePlay);
playBtn2.addEventListener('click', togglePlay);

// ------------------- Prev/Next -------------------
function prevSong(){ loadSong((currentIndex-1+songs.length)%songs.length); }
function nextSong(){ loadSong((currentIndex+1)%songs.length); }

prevBtn.addEventListener('click', prevSong);
nextBtn.addEventListener('click', nextSong);
prevBtn2.addEventListener('click', prevSong);
nextBtn2.addEventListener('click', nextSong);

// ------------------- Progress Bar -------------------
audio.addEventListener('timeupdate', ()=>{
  const progress = (audio.currentTime/audio.duration)*100;
  progressBar.value = progress || 0;
  if(currentTimeEl) currentTimeEl.textContent = formatTime(audio.currentTime);
  if(durationEl) durationEl.textContent = formatTime(audio.duration);
});

progressBar.addEventListener('input', ()=>{
  audio.currentTime = (progressBar.value/100)*audio.duration;
});

function formatTime(sec){
  if(!sec || isNaN(sec)) return "0:00";
  const m = Math.floor(sec/60);
  const s = Math.floor(sec%60).toString().padStart(2,'0');
  return `${m}:${s}`;
}

// ------------------- Load first song -------------------
loadSong(currentIndex);

// ------------------- Handle gestures -------------------
function handleGesture(gestureName){
  console.log("🎯 Gesture detected:", gestureName);
  switch(gestureName){

    // Static gestures
    case 'palm': if(audio.paused) togglePlay(); break;
    case 'fist': if(!audio.paused) togglePlay(); break;
    case 'index': nextSong(); break;
    case 'two_fingers': prevSong(); break;
    case 'thumbs_up': audio.volume = Math.min(audio.volume + 0.1, 1); break;
    case 'thumbs_down': audio.volume = Math.max(audio.volume - 0.1, 0); break;
    case 'mute': audio.muted = !audio.muted; break;

    // Swipe gestures
    case 'swipe_left': prevSong(); break;
    case 'swipe_right': nextSong(); break;
    case 'swipe_up': audio.volume = Math.min(audio.volume + 0.1, 1); break;
    case 'swipe_down': audio.volume = Math.max(audio.volume - 0.1, 0); break;
  }
}

// ------------------- Logout (robust) -------------------
document.addEventListener('DOMContentLoaded', () => {
  const logoutBtn = document.getElementById('logout-btn');
  if (!logoutBtn) return;

  logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();
    console.log("Logout clicked → redirecting");
    localStorage.removeItem("token");
    window.location.href = "/login/";
  });
});

// ------------------- Gesture Overlay -------------------
function showGestureOverlay(gesture) {
  const overlay = document.getElementById('gesture-overlay');
  if (!overlay) return;

  overlay.innerText = `🎯 ${gesture}`;
  overlay.classList.add('show');

  clearTimeout(overlay.removeTimer);
  overlay.removeTimer = setTimeout(() => {
    overlay.classList.remove('show');
  }, 1500);
}
