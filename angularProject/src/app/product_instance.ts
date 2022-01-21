import {Product} from "./product";

export class ProductInstance {
  id: number;
  product: Product;
  quantity: number;
  client: number;
  sale: number;
  sold: boolean;


  constructor(id: number, product: Product, quantity: number, client: number, sale: number, sold: boolean) {
    this.id = id;
    this.product = product;
    this.quantity = quantity;
    this.client = client;
    this.sale = sale;
    this.sold = sold;
  }

  price(): number {
    return this.quantity * this.product.price
  }

}
