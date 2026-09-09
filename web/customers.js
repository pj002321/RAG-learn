const filterInput = document.getElementById("filter");
const countBox = document.getElementById("count");
const listBox = document.getElementById("customer-list");
const emptyBox = document.getElementById("empty");
const detailBox = document.getElementById("detail");
const rawTable = document.getElementById("raw-info");
const maskedTable = document.getElementById("masked-info");
const purchaseLabel = document.getElementById("purchase-label");
const purchaseBox = document.getElementById("purchases");
const reviewLabel = document.getElementById("review-label");
const reviewBox = document.getElementById("reviews");
let allCustomers = [];

let selectedId = "";

// 서버에서 고객 목록을 받아 저장하고 첫 목록을 그립니다.
async function loadCustomers() {
  // 서버에 요청을 보내고 응답이 올 때까지 이 함수의 다음 처리를 기다립니다.
  const response = await fetch("/customers?limit=300");
  // 응답 본문을 JavaScript에서 읽을 수 있는 데이터로 바꿉니다.
  allCustomers = await response.json();
  // 받아오거나 검색으로 걸러낸 목록을 다시 그립니다.
  drawList(allCustomers);
}

// 고객 한 명을 표시할 버튼 HTML을 만듭니다. 이름은 escapeHtml로 처리합니다.
function customerRow(customer) {
  const sub = [customer.customer_id, customer.city, customer.skin_type].join(" · ");
  return `
    <button class="customer-item" data-id="${customer.customer_id}">
      <strong>${escapeHtml(customer.name)}</strong>
      <span class="sub">${escapeHtml(sub)}</span>
    </button>`;
}

// 목록의 각 항목을 HTML로 바꿔 목록 상자에 한꺼번에 표시합니다.
function drawList(customers) {
  countBox.textContent = "고객 " + customers.length + "명";
  // 고객마다 customerRow를 호출해 버튼을 만들고, 목록으로 이어 붙입니다.
  listBox.innerHTML = customers.map(customerRow).join("");
}

// 클릭할 때 아래 처리를 실행하도록 연결합니다. 지금 호출하는 것은 아닙니다.
listBox.addEventListener("click", function (event) {
  const item = event.target.closest(".customer-item");
  if (item) {
    // 누른 버튼의 고객 번호로 상세 조회를 시작합니다.
    selectCustomer(item.dataset.id);
  }
});

// 선택한 고객의 상세 정보를 받아 오른쪽 화면을 갱신합니다.
async function selectCustomer(customerId) {
  document.querySelectorAll(".customer-item").forEach(function (item) {
    item.classList.toggle("selected", item.dataset.id === customerId);
  });

  // 서버에 요청을 보내고 응답이 올 때까지 이 함수의 다음 처리를 기다립니다.
  const response = await fetch("/customers/" + customerId);
  // 응답 본문을 JavaScript에서 읽을 수 있는 데이터로 바꿉니다.
  const detail = await response.json();

  selectedId = customerId;
  // 서버에서 받은 상세 정보를 화면의 각 영역에 채웁니다.
  drawDetail(detail);
  emptyBox.classList.add("hidden");
  detailBox.classList.remove("hidden");
}

// 받은 정보를 항목별 표로 표시합니다.
function drawInfoTable(table, info) {
  const rows = [
    ["고객 번호", info.customer_id],
    ["이름", info.name],
    ["나이 / 성별", info.age + "세 / " + info.gender],
    ["피부 타입", info.skin_type],
    ["지역", info.city],
    ["전화번호", info.phone],
    ["이메일", info.email],
    ["가입일", info.joined_at],
  ];

  table.innerHTML = rows
    .map(([label, value]) => `<tr><th>${label}</th><td>${escapeHtml(value)}</td></tr>`)
    .join("");
}

// 구매 내역과 합계 금액을 표시합니다.
function drawPurchases(purchases, totalSpend) {
  purchaseLabel.textContent =
    "구매 내역 " + purchases.length + "건 · 합계 " + totalSpend.toLocaleString() + "원";
  purchaseBox.innerHTML = purchases
    .map(
      (purchase) => `
    <div class="row">
      <span class="row-date">${purchase.purchased_at}</span>
      <span class="row-main">${escapeHtml(purchase.product_name)}</span>
      <span class="row-side">${purchase.price.toLocaleString()}원 × ${purchase.quantity}</span>
    </div>`
    )
    .join("");
}

// 상품별 후기 내용과 평점을 표시합니다.
function drawReviews(reviews) {
  reviewLabel.textContent = "후기 " + reviews.length + "건";
  reviewBox.innerHTML = reviews
    .map(
      (review) => `
    <div class="row">
      <span class="row-date">${review.written_at}</span>
      <span class="row-main">
        <strong>${escapeHtml(review.product_name)}</strong>
        <span class="stars">${"★".repeat(review.rating)}</span>
        <span class="review-text">${escapeHtml(review.content)}</span>
      </span>
    </div>`
    )
    .join("");
}

// 상세 정보를 나누어 각 영역을 그리는 함수에 전달합니다.
function drawDetail(detail) {
  // 전달한 정보를 표에 채웁니다.
  drawInfoTable(rawTable, detail.customer);
  // 전달한 정보를 표에 채웁니다.
  drawInfoTable(maskedTable, detail.masked);
  // 구매 목록과 합계 금액을 구매 영역에 채웁니다.
  drawPurchases(detail.purchases, detail.total_spend);
  // 후기 목록을 후기 영역에 채웁니다.
  drawReviews(detail.reviews);
}

// 검색어가 바뀔 때 저장해 둔 목록을 걸러 다시 그리도록 연결합니다.
filterInput.addEventListener("input", function () {
  const word = filterInput.value.trim();
  const found = allCustomers.filter(function (customer) {
    return customer.name.includes(word) || customer.city.includes(word);
  });
  // 받아오거나 검색으로 걸러낸 목록을 다시 그립니다.
  drawList(found);
});

// 페이지를 열면 고객 목록을 한 번 불러옵니다.
loadCustomers();