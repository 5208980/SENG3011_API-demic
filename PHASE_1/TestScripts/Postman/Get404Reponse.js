// No Result Request (404)
// http://127.0.0.1:5000/v1.1/articles?start_date=2009-01-01T12:00:00&end_date=2009-02-01T12:00:00&location=australia&key_term=flu

// start_date=2009-01-01T12:00:00
// end_date=2009-02-01T12:00:00
// location=australia
// key_term=flu

pm.test("Status test", function () {
    pm.response.to.have.status(404);
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

pm.test("Message should be: No result for query", function () {
    pm.expect(pm.response.json().message).to.eql("No result for query");
});
