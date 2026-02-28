document.addEventListener("DOMContentLoaded", () => {
    const BASE_URL = "/api/users/";

    // Elements
    const loginBtn = document.getElementById("login-btn");
    const signupBtn = document.getElementById("signup-btn");
    const formTitle = document.getElementById("form-title");
    const authForm = document.getElementById("auth-form");
    const submitBtn = document.getElementById("submit-btn");

    const signupFields = document.getElementById("signup-extra-fields");
    const confirmPassword = document.getElementById("confirm-password");

    const loginCard = document.getElementById("login-card");
    const dashboardCard = document.getElementById("dashboard-card");
    const userName = document.getElementById("user-name");

    const modal = document.getElementById("modal");
    const modalText = document.getElementById("modal-text");
    const closeModal = document.getElementById("close-modal");

    /* ---------------------- TOGGLE LOGIN & SIGNUP ---------------------- */
    loginBtn.addEventListener("click", () => {
        loginBtn.classList.add("active");
        signupBtn.classList.remove("active");
        formTitle.textContent = "Login";

        signupFields.style.display = "none";
        confirmPassword.style.display = "none";

        submitBtn.textContent = "Login";
    });

    signupBtn.addEventListener("click", () => {
        signupBtn.classList.add("active");
        loginBtn.classList.remove("active");
        formTitle.textContent = "Sign Up";

        signupFields.style.display = "block";
        confirmPassword.style.display = "block";

        submitBtn.textContent = "Sign Up";
    });

    /* --------------------------- FORM SUBMIT --------------------------- */
    authForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const mode = formTitle.textContent.toLowerCase();
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (mode === "login") {
            await loginUser(username, password);

        } else {
            const full_name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const mobile = document.getElementById("mobile").value.trim();
            const confirm = confirmPassword.value.trim();

            if (password !== confirm) {
                alert("Passwords do not match!");
                return;
            }

            await registerUser({
                full_name: full_name,
                username: username,
                email: email,
                mobile: mobile,
                password: password,
                confirm_password: confirm
            });
        }
    });

    /* ----------------------------- LOGIN ----------------------------- */
    async function loginUser(username, password) {
        try {
            const res = await fetch(`${BASE_URL}login/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: username,   // IMPORTANT FIX
                    password: password
                }),
            });

            const data = await res.json();

            if (res.ok) {
                alert("Login successful!");
                localStorage.setItem("token", data.token);
                showDashboard(data.email ?? username);
            } else {
                alert(data.non_field_errors?.[0] || data.error || "Invalid login credentials");
            }

        } catch (error) {
            console.log("Login Error →", error);
            alert("Server not responding!");
        }
    }

    /* ----------------------------- SIGNUP ----------------------------- */
    async function registerUser(userData) {
        try {
            const res = await fetch(`${BASE_URL}register/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userData),
            });

            const data = await res.json();

            if (res.ok) {
                alert("Signup successful! Login now.");
                loginBtn.click();

            } else {
                alert(JSON.stringify(data) || "Signup failed");
            }

        } catch (error) {
            console.log("Signup Error →", error);
        }
    }

    /* ------------------------- SHOW DASHBOARD ------------------------- */
    function showDashboard(name) {
        loginCard.style.display = "none";
        dashboardCard.style.display = "flex";

        userName.textContent = name;
    }

    /* ------------------------- BLUETOOTH MODAL ------------------------- */
    document.getElementById("connect-new").addEventListener("click", async () => {
        modal.style.display = "flex";
        modalText.textContent = "Scanning for Bluetooth devices...";

        try {
            const device = await navigator.bluetooth.requestDevice({
                acceptAllDevices: true,
            });

            modalText.textContent = `Connected to: ${device.name}`;
        } catch (error) {
            modalText.textContent = "❌ No device connected!";
        }
    });

    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.onclick = (e) => {
        if (e.target === modal) modal.style.display = "none";
    };

    /* ----------------------- GO TO MUSIC PLAYER ----------------------- */
    document.getElementById("get-started").addEventListener("click", () => {
        window.location.href = "/music/";
    });
});
