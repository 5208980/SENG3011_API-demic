// Invalid Date Request (400)
// https://api-demic.herokuapp.com/articles?start_date=2020-01-0112:00:00&end_date=2020-02-01&location=australia&key_term=coronavirus

// start_date=2020-01-0112:00:00
// end_date=2020-02-01
// location=australia
// key_term=coronavirus

pm.test("Status test", function () {
    pm.response.to.have.status(400);
});

pm.test("Content-Type header is present", function () {
    pm.response.to.have.header("Content-Type");
});

pm.test("Returns Json", function () {
    pm.response.to.be.json;
});

pm.test("Json contains", function () {
    pm.expect(pm.response.text()).to.include("message");
});

pm.test("Message should be: Invalid Query Parameters (Date)", function () {
    pm.expect(pm.response.json().message).to.eql("Invalid Query Parameters (Date)");
});
