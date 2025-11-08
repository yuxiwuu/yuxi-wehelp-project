document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#login-form");
  const agree = document.querySelector("#agree");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!agree.checked) {
      alert("請勾選同意條款");
      return;
    }

    const formData = new FormData(form);

    const response = await fetch("/login", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.ok == true) {
      window.location.href = "/member";
    } else {
      window.location.href = "/ohoh?msg=" + data.msg;
    }
  });

  const hotelForm = document.querySelector("#hotel-form");
  const input = document.querySelector("#hotel-id");
  if (!input || !hotelForm) return;

  hotelForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const raw = input.value.trim();
    const num = Number(raw);
    if (!Number.isInteger(num) || num <= 0) {
      alert("請輸入正整數");
      return;
    }
    window.location.href = "/hotel/" + raw;
  });
});
