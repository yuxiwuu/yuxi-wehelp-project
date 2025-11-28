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

  const searchMember = document.querySelector("#search_btn");
  const input = document.querySelector("#search_id");
  const result = document.querySelector("#searchResult");

  searchMember.addEventListener("click", async (e) => {
    const id = input.value.trim();

    const response = await fetch(`/api/member/${id}`);
    const json = await response.json();

    if (json.data == null) {
      result.textContent = "No Data";
    } else {
      result.textContent = `${json.data.name} (${json.data.email})`;
    }

    input.value = "";
  });

  const updateName = document.querySelector("#update_btn");
  const nameInput = document.querySelector("#update_name");
  const updateMsg = document.querySelector("#updateMsg");
  const welcomeName = document.querySelector("#welcome_name");

  updateName.addEventListener("click", async (e) => {
    e.preventDefault();

    const newName = nameInput.value.trim();
    const response = await fetch("/api/member", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: newName,
      }),
    });
    const data = await response.json();

    if (data.ok == true) {
      updateMsg.textContent = "更新成功";
      welcomeName.textContent = newName;
    } else if (data.error == true) {
      if (data.msg) {
        updateMsg.textContent = "更新失敗:" + data.msg;
      } else {
        updateMsg.textContent = "更新失敗";
      }
    }
    nameInput.value = "";
  });

  const renewSearcher = document.querySelector("#renew_btn");
  const searcherName = document.querySelector("#searchedResault");

  renewSearcher.addEventListener("click", async (e) => {
    e.preventDefault();

    const response = await fetch("/api/member/search_log");
    const json = await response.json();

    if (!json.data || json.data.length == 0) {
      searcherName.textContent = "目前沒有查詢記錄";
      return;
    } else {
      const lines = json.data.map((log) => {
        return `${log.name} (${log.time})`;
      });
      searcherName.innerHTML = lines.join("<br>");
    }
  });
});
