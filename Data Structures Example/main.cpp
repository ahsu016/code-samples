#include <iomanip>
#include <iostream>
#include <memory>
#include <utility>
#include <vector>
#include <iterator>

#include "GroceryItem.hpp"

int main() {

std::cout   << std::showpoint << std::fixed << std::setprecision(2)             //for floating point values
            << "Welcome to Kroger.  Place grocery items into your shopping cart by entering each item's information.\n"
            << "   enclose string entries in quotes, separate fields with comas\n"
            << "   for example:  \"00016000306707\", \"Betty Crocker\", \"Betty Crocker Double Chocolate Chunk Cookie Mix\", 17.19\n"
            << "   Enter CTL-Z (Windows) or CTL-D (Linux) to quit\n\n";

std::vector<std::unique_ptr<GroceryItem>>cart;                                  //unique pointer vector for grocery cart

GroceryItem item;

while(std::cout     << "Enter UPC, Product Brand, Product Name, and Price\n", std::cin >> item)
{
    cart.push_back(std::make_unique<GroceryItem> (std::move(item)));            //appends to end of cart
    std::cout << "Item added to shopping cart: " << *cart.back() << "\n"; //prints item info 
}  

std::cout << "\n\nHere is an itemized list of the items in your shopping cart:\n";

for(auto groc = cart.crbegin(); groc < cart.crend(); ++groc)
    std::cout << **groc;

return 0;
}
