function uiUpdate() {
  // Lấy các element
  const actionRadios = document.getElementsByName("action");
  let action = "encrypt";
  for (const radio of actionRadios) {
    if (radio.checked) action = radio.value;
  }

  const mode = document.getElementById("mode").value;
  const ivGroup = document.getElementById("iv-group");
  const inputLabel = document.getElementById("input-label");
  const inputField = document.getElementById("input_text");

  // Cập nhật class active cho radio button
  document.querySelectorAll(".option-card").forEach((card) => {
    if (card.querySelector("input").checked) {
      card.classList.add("active");
    } else {
      card.classList.remove("active");
    }
  });

  // LOGIC ẨN HIỆN IV
  // IV chỉ cần nhập thủ công khi: Mode = CBC VÀ Action = Decrypt
  if (mode === "CBC" && action === "decrypt") {
    ivGroup.style.display = "block";
  } else {
    ivGroup.style.display = "none";
  }

  // LOGIC THAY ĐỔI LABEL
  if (action === "encrypt") {
    inputLabel.innerText = "Văn bản cần mã hóa (Plaintext):";
    inputField.placeholder = "Ví dụ: Hello DES...";
  } else {
    inputLabel.innerText = "Chuỗi mã hóa (Ciphertext - Hex):";
    inputField.placeholder = "Ví dụ: a1b2c3d4...";
  }
}
