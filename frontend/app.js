document.addEventListener("DOMContentLoaded", () => {
  const article = document.querySelector(".post");
  const next = document.querySelector(".next");
  const previous = document.querySelector(".previous");
  let art = {};
  function navigate(page) {
    fillPage(undefined, undefined, page);
  }
  previous.addEventListener("click", () => {
    navigate(art.previous);
  });
  next.addEventListener("click", () => {
    navigate(art.next);
  });
  function fillPage(sort, search, page) {
    let baseUrl = `http://127.0.0.1:8000/posts/`;
    let normalUrl = search ? `${baseUrl}?title=${search}` : baseUrl;
    const url = page ? page : normalUrl;
    fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
      .then((resp) => {
        if (!resp.ok) {
          console.log(resp);
          throw new Error("failed to fetch");
        }
        return resp.json();
      })
      .then((articles) => {
        art = articles;
        let posts;
        if (sort === "ranking") {
          posts = [...articles.results].sort((a, b) => a.ranking - b.ranking);
        } else if (sort === "comments") {
          console.log("comments");
          posts = [...articles.results].sort(
            (a, b) => b.post[0].comments - a.post[0].comments
          );
        } else if (sort === "points") {
          posts = [...articles.results].sort(
            (a, b) => b.post[0].points - a.post[0].points
          );
        } else {
          posts = [...articles.results].sort((a, b) => a.ranking - b.ranking);
        }
        const postMainBody = document.querySelector(".post");

        while (postMainBody.firstChild) {
          postMainBody.removeChild(postMainBody.firstChild);
        }
        for (const post of posts) {
          const postDiv = document.createElement("div");
          postDiv.classList.add("post_div");
          const rank = document.createElement("div");
          rank.textContent = post.ranking + ".";
          const postBody = document.createElement("div");
          const title = document.createElement("p");
          const titleUrl = document.createElement("a");
          titleUrl.href = post.title_url;
          title.textContent = post.title + ` (${post.source})`;
          const postMeta = document.createElement("div");
          postMeta.classList.add("post_meta");
          const writer = document.createElement("p");
          writer.textContent = post.post[0].writer;
          const time = document.createElement("p");
          time.textContent = `time ${post.time} |`;
          const points = document.createElement("p");
          points.textContent = `points ${post.post[0].points} |`;
          const comments = document.createElement("p");
          comments.textContent = `comments ${post.post[0].comments}`;
          postMeta.appendChild(writer);
          postMeta.appendChild(time);
          postMeta.appendChild(points);
          postMeta.appendChild(comments);
          titleUrl.appendChild(title);
          postBody.appendChild(titleUrl);
          postBody.appendChild(postMeta);
          postDiv.appendChild(rank);
          postDiv.appendChild(postBody);
          article.appendChild(postDiv);
        }

        if (articles.next === null && articles.previous === null) {
          next.classList.remove("show-btn");
          previous.classList.remove("show-btn");
        } else if (articles.next !== null && articles.previous !== null) {
          next.classList.add("show-btn");
          previous.classList.add("show-btn");
        } else if (articles.next !== null && articles.previous === null) {
          next.classList.add("show-btn");
          previous.classList.remove("show-btn");
        } else {
          next.classList.remove("show-btn");
          previous.classList.add("show-btn");
        }
      });
  }
  fillPage();
  console.log(art);

  let debouncer;
  const searchBtn = document.querySelector(".search");
  searchBtn.addEventListener("input", (e) => {
    clearTimeout(debouncer);
    debouncer = setTimeout(() => {
      fillPage(undefined, searchBtn.value);
    }, 300);
  });

  const sortList = document.querySelector(".sort-list");
  sortList.addEventListener("click", (e) => {
    const items = document.querySelectorAll(".sort-list >*");
    if (!sortList.classList.contains("show")) {
      sortList.classList.toggle("show");
      return;
    }
    items.forEach((item) => {
      item.classList.remove("selected-sort-order");
    });
    e.target.classList.add("selected-sort-order");
    fillPage(e.target.textContent);
    sortList.classList.toggle("show");
  });
});
