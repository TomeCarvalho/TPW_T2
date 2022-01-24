import { Component, OnInit } from '@angular/core';
import {Product} from "../product";
import {ProductInstance} from "../product_instance";
import {CartService} from "../cart.service";

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit {

  cart!: ProductInstance[];

  constructor(private cartService: CartService) { }

  ngOnInit(): void {
    this.cartService.getCart().subscribe(value => {this.cart = value;console.log("CART"); console.log(this.cart)})
  }

  getTotal(){
    let total = 0
    for (let p of this.cart){
      console.log(p)
      total += p.quantity * p.product.price
    }
    return total
  }

  remove(obj: ProductInstance): void{
    const index = this.cart.indexOf(obj, 0);
    if (index > -1) {
      this.cart.splice(index, 1);
    }
    this.cartService.deleteInstance(obj);
  }

}
