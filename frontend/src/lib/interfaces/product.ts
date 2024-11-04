export interface Product {
    id: number;
    title: string;
    price: number;
    height: number;
    width: number;
    medium: "Painting" | "Print";
    imageUrl: string;
}