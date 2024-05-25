export const load = async ({ fetch }) => {
    const fetchProducts = async () => {
        const response = await fetch(`http://127.0.0.1:8000/products`);

        if (response.status !== 200) {
            console.log("Error retrieving products.");
        }
    
        const responseData = await response.json();
        
        return responseData;
    }

    return {
        products: fetchProducts()
    }
}