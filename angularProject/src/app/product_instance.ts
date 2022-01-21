import {Product} from "./product";

export class ProductInstance {
  product: Product;
  quantity: number;
  client: number;
  sale: number;
  sold: boolean;


  constructor(product: Product, quantity: number, client: number, sale: number, sold: boolean) {
    console.log(product)
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
