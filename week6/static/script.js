document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.querySelector("#signup_form");

  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(signupForm);
      const name = formData.get("name");
      const email = formData.get("email");
      const password = formData.get("password");

      const response = await fetch("/signup", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (data.ok) {
        signupForm.reset();
        window.location.href = "/";
      } else {
        window.location.href = "/ohoh?msg=" + data.msg;
      }
    });
  }

  const loginForm = document.querySelector("#login_form");

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(loginForm);
      const email = formData.get("email");
      const password = formData.get("password");

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
  }

  const deleteButtons = document.querySelectorAll(".delete_btn");

  deleteButtons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const messageId = btn.dataset.id;
      const ok = confirm("確定要刪除嗎？");
      if (!ok) {
        e.preventDefault();
      }

      const formData = new FormData();
      formData.append("message_id", messageId);
      const response = await fetch("/deleteMessage", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (data.ok == true) {
        window.location.reload();
      }
    });
  });
});
