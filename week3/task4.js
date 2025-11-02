document.addEventListener("DOMContentLoaded", async () => {
  const url1 = "https://cwpeng.github.io/test/assignment-3-1";
  const url2 = "https://cwpeng.github.io/test/assignment-3-2";

  const [textRes, imgRes] = await Promise.all([fetch(url1), fetch(url2)]);
  const textData = await textRes.json();
  const imgData = await imgRes.json();

  const host = imgData.host;
  const imgMap = {};
  for (let r of imgData.rows) {
    imgMap[r.serial] = firstImage(host, r.pics);
  }

  const merged = textData.rows.map((r) => ({
    title: r.sname,
    img: imgMap[r.serial],
  }));

  render(merged);
  renderLoadMore(merged);
});

function firstImage(host, pics) {
  if (!pics || typeof pics !== "string") {
    return "";
  }
  const first = pics.split(".jpg")[0] + ".jpg";
  return host + first;
}

function render(data) {
  const barSection = document.querySelector(".bars");
  const cardSection = document.querySelector(".cards");

  barSection.textContent = "";
  cardSection.textContent = "";

  for (let i = 0; i < 3; i++) {
    barSection.appendChild(createBarContent(data[i], i + 1));
  }
  for (let i = 3; i < 13; i++) {
    const card = createCardContent(data[i]);
    cardSection.appendChild(card);
  }
}

function createBarContent(attraction, index) {
  let container = document.createElement("div");
  container.className = "bar bar" + index;
  let img = document.createElement("img");
  img.src = attraction.img;
  container.appendChild(img);

  let text = document.createElement("div");
  text.className = "bar_text";
  text.textContent = attraction.title;
  container.appendChild(text);

  return container;
}

function createCardContent(attraction) {
  let container = document.createElement("div");
  container.className = "card";

  let img = document.createElement("img");
  img.src = attraction.img;
  container.appendChild(img);

  let star = document.createElement("div");
  star.className = "star_icon";
  let starImg = document.createElement("img");
  starImg.src = "../week1/image/star-solid.svg";
  star.appendChild(starImg);
  container.appendChild(star);

  let overlay = document.createElement("div");
  overlay.className = "card_overlay";
  let text = document.createElement("div");
  text.className = "card_title";
  text.textContent = attraction.title;

  overlay.appendChild(text);
  container.appendChild(overlay);

  return container;
}

function renderLoadMore(data) {
  const button = document.getElementById("loadMore");
  const cardsWrap = document.querySelector(".cards");
  let currentIndex = 13;

  button.addEventListener("click", () => {
    const nextAmount = data.slice(currentIndex, currentIndex + 10);
    nextAmount.forEach((item) => {
      const card = createCardContent(item);
      cardsWrap.appendChild(card);
    });
    currentIndex += 10;

    if (currentIndex >= data.length) {
      button.style.display = "none";
    }
  });
}
