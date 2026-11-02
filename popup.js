"use strict";

const queryInput = document.querySelector("#query");
const setupToggle = document.querySelector("#setup-toggle");
const setupPanel = document.querySelector("#setup");
const copyStatus = document.querySelector("#copy-status");

queryInput.focus();

setupToggle.addEventListener("click", () => {
  const isOpen = setupToggle.getAttribute("aria-expanded") === "true";
  setupToggle.setAttribute("aria-expanded", String(!isOpen));
  setupPanel.hidden = isOpen;
});

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    // Clipboard API can be unavailable in some extension contexts.
    const field = document.createElement("textarea");
    field.value = text;
    field.setAttribute("readonly", "");
    document.body.append(field);
    field.select();
    document.execCommand("copy");
    field.remove();
  }
}

for (const button of document.querySelectorAll("[data-copy]")) {
  button.addEventListener("click", async () => {
    const original = button.textContent;

    try {
      await copyText(button.dataset.copy);
    } catch {
      copyStatus.textContent = "Could not copy. Select the value and copy it manually.";
      return;
    }

    button.textContent = "Copied";
    copyStatus.textContent = `${button.dataset.label} copied to the clipboard.`;
    setTimeout(() => {
      button.textContent = original;
    }, 1500);
  });
}
