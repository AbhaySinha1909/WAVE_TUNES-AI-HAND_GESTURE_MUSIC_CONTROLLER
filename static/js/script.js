/* -------------------------------
   MOBILE MENU TOGGLE (Optional)
--------------------------------*/
const menuBtn = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");

if (menuBtn) {
    menuBtn.addEventListener("click", () => {
        nav.classList.toggle("active");
    });
}

/* -------------------------------
   SMOOTH SCROLLING FOR NAV LINKS
--------------------------------*/
document.querySelectorAll('.nav a[href^="#"]').forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();

        const target = document.querySelector(link.getAttribute("href"));
        if (target) {
            target.scrollIntoView({ behavior: "smooth" });
        }
    });
});

/* -------------------------------
   FADE-IN ANIMATION WHEN SCROLLING
--------------------------------*/
const observer = new IntersectionObserver(
    entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    },
    { threshold: 0.2 }
);

document.querySelectorAll("section").forEach(section => {
    section.classList.add("fade-section");
    observer.observe(section);
});

/* -------------------------------
   LOGIN STATUS CHECK (BACKEND API)
--------------------------------*/
const API_BASE = "/api/users/";

async function checkLoginStatus() {
    try {
        const response = await fetch(API_BASE, {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            const user = await response.json();
            console.log("Logged in:", user);

            const loginBtn = document.querySelector(".login-btn");
            if (loginBtn) {
                loginBtn.textContent = user.username || "Dashboard";
                loginBtn.href = "/dashboard/";
            }
        }
    } catch (error) {
        console.log("User not logged in.");
    }
}

checkLoginStatus();

/* -------------------------------
   STICKY NAVBAR SHADOW (Optional)
--------------------------------*/
window.addEventListener("scroll", () => {
    const navbar = document.querySelector(".navbar");
    if (window.scrollY > 20) {
        navbar.style.boxShadow = "0 0 15px rgba(0,0,0,0.5)";
    } else {
        navbar.style.boxShadow = "none";
    }
});
