interface Product {
    id: number;
    title: string;
    price: number;
    height: number;
    width: number;
    medium: "Painting" | "Print";
    thumbnail: string;
}

export interface ProductsOut extends Product {
    imageUrl: string;
}

export interface ProductOut extends Product {
    description: string | null;
    images: string[];
}