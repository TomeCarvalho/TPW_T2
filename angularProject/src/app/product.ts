export class Product {
  id: number;
  images: any[];
  category: string;
  name: string;
  stock: number;
  description: string;
  price: number;
  hidden: boolean;
  seller: number;
  group: any[];


  constructor(id: number, images: any[],
              category: string, name: string,
              stock: number, description: string,
              price: number, hidden: boolean,
              seller: number, group: any[]) {
    this.id = id;
    this.images = images;
    this.category = category;
    this.name = name;
    this.stock = stock;
    this.description = description;
    this.price = price;
    this.hidden = hidden;
    this.seller = seller;
    this.group = group;
  }
}
