document.addEventListener("DOMContentLoaded", function () {
  // Check if the loading screen has been displayed before
  if (localStorage.getItem("loadingScreenDisplayed") !== "true") {
    // Set the flag in localStorage
    localStorage.setItem("loadingScreenDisplayed", "true");

    // Apply the fade-in animation to the body
    document.body.style.animation = "fadeIn 1s ease-out 1 both";
  } else {
    // If the loading screen has been displayed before, show the body immediately
    document.body.style.opacity = "1";
  }
});
