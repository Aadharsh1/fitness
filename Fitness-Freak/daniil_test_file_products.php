<html>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <h1>This is the product page</h1>
</html>
<?php
session_start();
// Make a GET request to the microservices API endpoint
$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/product');
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($curl);
curl_close($curl);

// Parse the JSON response
$data = json_decode($response, true);

// Check if JSON decoding was successful
if ($data === null) {
    echo "Error: Failed to decode JSON response.";
} else {
    // Display the data on the PHP page
    echo "
    <div class='container'>
        <div class='row row-cols-1 row-cols-md-2 g-4'>
    ";
    foreach ($data['data']['products'] as $item) {
        echo 
        "<div class='col'>"
        . "<img src='" . $item['image'] . "' width='100' height='100'>"
        . "<table border='1'>"
        . "<tr> <td>Title:</td><td>" . $item['title'] . "</td></tr>"
        . "<tr> <td>Description:</td><td>" . $item['description'] . "</td></tr>"
        . "<tr> <td>ID:</td><td>" . $item['id'] . "</td></tr>"
        . "<tr> <td>Price:</td><td>" . $item['price'] . "</td></tr>"
        . "<tr> <td>Availability:</td><td>" . $item['availability'] . "</td></tr>"
        . "</table>"
        . "</div>";
    }
    echo "</div>";
}
?>