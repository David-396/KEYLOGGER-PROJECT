let attempts = 0;
const maxAttempts = 3;

// פונקציה לשינוי סוג הקלט (הצגת סיסמה/הסתרה)
function togglePassword() {
  const passwordInput = document.getElementById('password');
  passwordInput.type = (passwordInput.type === 'password') ? 'text' : 'password';
}

// פונקציה לטיפול בלחיצה על "היכנס"
function login() {
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  const messageDiv = document.getElementById('message');
  
  // ניקוי הודעות קודמות
  messageDiv.textContent = '';
  
  // בדיקת קלט בסיסיות
  if (!username && !password) {
    messageDiv.textContent = "הזן שם וסיסמה";
    return;
  }
  
  if (!username) {
    messageDiv.textContent = "הזן שם משתמש";
    return;
  }
  
  if (!password) {
    messageDiv.textContent = "הזן סיסמה";
    return;
  }
  
  if (password.length < 4) {
    messageDiv.textContent = "הסיסמה צריכה להיות לפחות 4 תווים";
    return;
  }
  
  // הכנה לקריאה לשרת
  const payload = { username, password };
  
  fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(data => {
    // טיפול בתשובות מהשרת
    if(data.status === 'blocked'){
      messageDiv.textContent = "חשבונך נחסם, פנה לרלשית";
    } else if(data.status === 'not_registered'){
      messageDiv.textContent = "המשתמש אינו רשום במערכת";
      attempts++;
    } else if(data.status === 'wrong_password'){
      messageDiv.textContent = "סיסמה שגויה";
      attempts++;
    } else if(data.status === 'success'){
      messageDiv.style.color = 'green';
      messageDiv.textContent = "יאללה, כנס בהם";
      // הפניה לדף המבוקש לאחר עיכוב קצר
      setTimeout(() => {
        window.location.href = "file:///C:/Users/User/Desktop/%D7%94%D7%A4%D7%A8%D7%95%D7%99%D7%99%D7%A7%D7%98%20%D7%A9%D7%9C%D7%99/front_berale/index.html";
      }, 1000);
    } else {
      messageDiv.textContent = "נסה שנית";
      attempts++;
    }
    
    // במקרה של 3 ניסיונות כושלים
    if(attempts >= maxAttempts && data.status !== 'success'){
      messageDiv.textContent = "חשבונך נחסם, פנה לרלשית";
    }
  })
  .catch(error => {
    console.error('Error:', error);
    messageDiv.textContent = "שגיאה בשרת, נסה שוב מאוחר יותר";
  });
}