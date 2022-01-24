import {Component, OnInit} from '@angular/core';
import {ProductService} from "../product.service";
import {Product} from "../product";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-listproducts',
  templateUrl: './listproducts.component.html',
  styleUrls: ['./listproducts.component.css']
})
export class ListproductsComponent implements OnInit {

  products_group: Product[][] | undefined;
  all_products: Product[] = [];
  source!: string;

  constructor(private productService: ProductService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {

    this.route.data.subscribe(value => {
      this.source = value['source']
      console.log(this.source)
      if( this.source == 'my-products' && localStorage.getItem('loginToken') == ''){
        this.router.navigate(['dashboard'])
        return
      }

      let query = ""
      this.route.queryParamMap.subscribe(params =>{
        console.log(params)
        query = this.getQuery(params)
        this.getProducts(query);
      })
      if (!query){
        this.getProducts("");
      }

    })

  }

  getProducts(query: string){
    this.productService.getProducts(this.source, query).subscribe(products => {
      this.all_products = products;
      this.products_group = this.groupByN(4, this.all_products);
    })
  }

  groupByN(n: number, data: Product[]) {
    console.log("AAAAAAAAA")
    console.log(data)
    let result = [];
    for (let i = 0; i < data.length; i += n) result.push(data.slice(i, i + n));
    console.log(result)
    return result;
  };

  getQuery(data: any) {
    if (!data){
      return ""
    }
    let query = "?";
    console.log("getQuery")
    console.log(data)
    for (let [key, value] of Object.entries(data.params)) {
      if (value) {
        console.log(value)
        query += `${key}=${value}&`;
      }
    }
    console.log(query)
    return query
  }

}
