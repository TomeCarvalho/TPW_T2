import { Component, OnInit } from '@angular/core';
import {ProductService} from "../product.service";
import {Product} from "../product";

@Component({
  selector: 'app-listproducts',
  templateUrl: './listproducts.component.html',
  styleUrls: ['./listproducts.component.css']
})
export class ListproductsComponent implements OnInit {

  products_group: Product[][] | undefined;
  all_products: Product[] = [];


  constructor(private productService: ProductService) { }

  async ngOnInit(): Promise<void> {


    await this.productService.getDashboard().subscribe(products => {
      console.log("I");
      this.all_products = products;
      this.products_group = this.groupByN(3, this.all_products);
    })
    console.log(this.all_products)
  }
  groupByN(n: number, data: Product[]) {
    console.log("AAAAAAAAA")
    console.log(data)
    let result = [];
    for (let i = 0; i < data.length; i += n) result.push(data.slice(i, i + n));
    console.log(result)
    return result;
  };

}
