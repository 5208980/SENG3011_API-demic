// Success Request
// https://api-demic.herokuapp.com/articles?start_date=2020-0&end_date=2020-02-01T12:00:00&location=australia&key_term=coronavirus

// start_date=2020-0
// end_date=2020-02-01T12:00:00
// location=australia
// key_term=coronavirus

pm.test("Status test", function () {
    pm.response.to.have.status(200);
});

pm.test("Content-Type header is present", function () {
    pm.response.to.have.header("Content-Type");
});

pm.test("Returns Json", function () {
    pm.response.to.be.json;
});

pm.test("Json contain articles", function () {
    pm.expect(pm.response.text()).to.include("articles");
});

pm.test("articles has url", function () {
    pm.expect(pm.response.text()).to.include("url");
});

pm.test("articles has reports", function () {
    pm.expect(pm.response.text()).to.include("reports");
});
