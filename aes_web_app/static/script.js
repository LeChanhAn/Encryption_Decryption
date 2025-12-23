function toggleIV(action) {
  const ivGroup = document.getElementById("iv-group");
  const inputLabel = document.getElementById("input-label");
  const inputField = document.querySelector('textarea[name="input_text"]');

  if (action === "encrypt") {
    ivGroup.style.display = "none";
    inputLabel.innerText = "Nội dung cần mã hóa (Plaintext):";
    inputField.placeholder = "Nhập văn bản tiếng Việt hoặc tiếng Anh...";
  } else {
    ivGroup.style.display = "block";
    inputLabel.innerText = "Chuỗi mã hóa (Ciphertext - Hex):";
    inputField.placeholder = "Ví dụ: 8a2f3d...";
  }
}
