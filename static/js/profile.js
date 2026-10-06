const profileImage = document.getElementById("profile-preview");
const profileInput = document.getElementById("profile_image");
const profileForm = document.getElementById("profile-form");
const imageArea = document.querySelector(".profile-image-area");
const imageOptions = document.getElementById("image-options");
const changeImage = document.getElementById("change-image");
const removeImage = document.getElementById("remove-image");

let hideMenuTimeout;

const showImageMenu = () => {
    clearTimeout(hideMenuTimeout);
    imageOptions?.classList.add("show");
};

const hideImageMenu = () => {
    hideMenuTimeout = setTimeout(() => {
        imageOptions?.classList.remove("show");
    }, 250);
};

if (imageArea && imageOptions) {
    imageArea.addEventListener("mouseenter", showImageMenu);
    imageArea.addEventListener("mouseleave", hideImageMenu);
    imageOptions.addEventListener("mouseenter", showImageMenu);
    imageOptions.addEventListener("mouseleave", hideImageMenu);
}

if (changeImage && profileInput) {
    changeImage.addEventListener("click", (event) => {
        event.preventDefault();
        clearTimeout(hideMenuTimeout);
        profileInput.click();
    });
}

if (profileInput) {
    profileInput.addEventListener("change", () => {
        const file = profileInput.files[0];

        if (!file) return;

        profileImage.src = URL.createObjectURL(file);
        profileForm.submit();
    });
}

if (removeImage) {
    removeImage.addEventListener("click", async (event) => {
        event.preventDefault();

        if (!window.confirm("Remove your profile picture?")) return;

        try {
            removeImage.disabled = true;

            const response = await fetch("/profile", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    remove_image: true
                })
            });

            if (!response.ok) {
                throw new Error("Unable to remove profile image");
            }

            window.location.reload();

        } catch (error) {
            console.error("Remove image error:", error);
            removeImage.disabled = false;
        }
    });
}