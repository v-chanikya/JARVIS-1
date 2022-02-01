let expDays = 1;

function setCookie(cName, cValue) {
        let date = new Date();
        date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = cName + "=" + cValue + "; " + expires + "; path=/";
}

function getCookie(cName) {
      const name = cName + "=";
      const cDecoded = decodeURIComponent(document.cookie); //to be careful
      const cArr = cDecoded .split('; ');
      let res;
      cArr.forEach(val => {
          if (val.indexOf(name) === 0) res = val.substring(name.length);
      })
      return res;
}

function delCookie(cName) {
        const expires = "expires=" + "Wed, 05 Aug 2020 23:00:00 UTC" ;
        document.cookie = cName + "= 0;" + expires + "; path=/";
}

function testCookie(){
    setCookie("hello", 1234);
    console.log(getCookie("hello"));
    delCookie("hello");
    console.log(getCookie("hello"));
}

function sessionCleanup(){
    delCookie("session_id");
    delCookie("user");
    window.location.href = "/";
}
