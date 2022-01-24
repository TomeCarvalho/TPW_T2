import { Component, OnInit } from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {PaymentService} from "../payment.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-paymentform',
  templateUrl: './paymentform.component.html',
  styleUrls: ['./paymentform.component.css']
})
export class PaymentformComponent implements OnInit {

  cards = [
    {name: "MasterCard", value: "MasterCard"},
    {name: "Visa", value: "Visa"},
    {name: "Paypal", value: "Paypal"},
  ]

  paymentForm = this.formBuilder.group({
    'card': '',
    'number': '',
    'date': '',
    'cvc': '',
    'name': ''
  })


  constructor(private formBuilder: FormBuilder,
              private paymentService: PaymentService,
              private router: Router) { }

  ngOnInit(): void {

  }

  onSubmit(data: any) {
    if (data){
      this.paymentService.checkout(data).then(
        () => {
          console.log("Checkout GOOD")
          this.router.navigate(['dashboard'])
        },
        () => {
          console.log("Checkout BAD");
          this.paymentForm.reset()
        }
      )
    }
  }

}
