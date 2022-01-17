export class Product {
  category: string;
  name: string;
  stock: number;
  description: string;
  price: number;
  seller: number;
  group: string
  hidden: boolean;

  constructor(category: string, name: string,
              stock: number, description: string,
              price: number, seller: number,
              group: string, hidden: boolean) {
    this.category = category;
    this.name = name;
    this.stock = stock;
    this.description = description;
    this.price = price;
    this.seller = seller;
    this.group = group;
    this.hidden = hidden;
  }
}
