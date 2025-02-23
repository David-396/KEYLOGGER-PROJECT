document.addEventListener("DOMContentLoaded", function() {
    const catButtons = document.querySelectorAll(".cat-btn");
    const catContents = document.querySelectorAll(".cat-content");
    let currentCategory = null;
    let searchHistory = [];
  
    function hideAllContents() {
      catContents.forEach(content => content.style.display = "none");
    }
    
    // מעבר בין קטגוריות
    catButtons.forEach(btn => {
      btn.addEventListener("click", function() {
        hideAllContents();
        const catId = btn.getAttribute("data-cat");
        currentCategory = catId;
        const contentDiv = document.getElementById(catId);
        if(contentDiv) {
          contentDiv.style.display = "block";
        }
      });
    });
    
    // טיפול בלחצני "הוספת" (לחיפוש נוסף)
    const addButtons = document.querySelectorAll(".add-btn");
    addButtons.forEach(btn => {
      btn.addEventListener("click", function() {
        const targetId = btn.getAttribute("data-target");
        const targetInput = document.getElementById(targetId);
        if(targetInput) {
          // שיבוט שדה קלט והוספתו מתחת לשדה המקורי
          let clone = targetInput.cloneNode(true);
          clone.value = "";
          targetInput.parentNode.insertBefore(clone, targetInput.nextSibling);
        }
      });
    });
    
    // כפתור ביצוע חיפוש – אוסף את הנתונים ומעדכן את ההיסטוריה
    const executeSearchBtn = document.getElementById("execute-search");
    executeSearchBtn.addEventListener("click", function() {
      if(!currentCategory) {
        alert("בחר קטגוריה תחילה.");
        return;
      }
      const currentContent = document.getElementById(currentCategory);
      const inputs = currentContent.querySelectorAll("input");
      const checkboxes = currentContent.querySelectorAll("input[type='checkbox']");
      let data = { category: currentCategory, inputs: [], checkboxes: [] };
      
      inputs.forEach(input => {
        data.inputs.push({ name: input.placeholder || input.id, value: input.value });
      });
      checkboxes.forEach(cb => {
        data.checkboxes.push({ label: cb.nextElementSibling ? cb.nextElementSibling.textContent : "", checked: cb.checked });
      });
      data.timestamp = new Date().toLocaleString();
      searchHistory.push(data);
      updateHistory();
      alert("חיפוש בוצע. הנתונים נרשמו בהיסטוריה.");
    });
    
    // עדכון רשימת ההיסטוריה
    function updateHistory() {
      const historyList = document.getElementById("history-list");
      if(historyList) {
        historyList.innerHTML = "";
        searchHistory.forEach((item, index) => {
          let btn = document.createElement("button");
          btn.classList.add("history-item");
          let summary = item.category;
          const checked = item.checkboxes.filter(cb => cb.checked).map(cb => cb.label);
          if(checked.length > 0) {
            summary += " / " + checked.join(" & ");
          }
          btn.textContent = summary + " - " + item.timestamp;
          btn.addEventListener("click", function() {
            alert("פרטי חיפוש:\n" + JSON.stringify(item, null, 2));
          });
          historyList.appendChild(btn);
        });
      }
    }
    
    // כפתור "חפש שנית" לניקוי השדות
    const searchAgainBtn = document.getElementById("search-again");
    if(searchAgainBtn) {
      searchAgainBtn.addEventListener("click", function() {
        if(currentCategory) {
          const currentContent = document.getElementById(currentCategory);
          const inputs = currentContent.querySelectorAll("input");
          inputs.forEach(input => input.value = "");
          const checkboxes = currentContent.querySelectorAll("input[type='checkbox']");
          checkboxes.forEach(cb => cb.checked = false);
        }
        alert("ניתן להתחיל חיפוש חדש.");
      });
    }
  });
  