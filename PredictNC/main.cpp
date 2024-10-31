#include <iostream>
#include <fstream>
#include <vector>
#include <map>

#include "regression_parameters.h"

using namespace std;

int number_of_appearances_of_key (
    string & current_SMILES_record,
    vector <string> & current_key )
{
    int number_of_appearances = 0;
    for ( int ii =0 ;ii < current_key.size(); ii++ )
    {
        size_t pos = 0;
        string cu_SMILES_local = current_SMILES_record;
        while ( ( pos = cu_SMILES_local.find(current_key[ii]) ) !=  std::string::npos )
        {
            number_of_appearances++;
            cu_SMILES_local= cu_SMILES_local.substr (pos+1);     // get from "live" to the end
        }
    }
    return number_of_appearances;
}


void mk_predictor_by_SMILES (
    string                          & cu_SMILES,
    vector <double>                 & predictors)
{
    int predictors_number = key_set.size();
    predictors.resize(predictors_number);

    for (int kk=0;kk<predictors_number;kk++)
    {
        int current_occurence_number    = number_of_appearances_of_key (
                                            cu_SMILES,
                                            key_set[kk]);

        predictors[kk]                  =   (double) current_occurence_number ;
     }
}

double calculate_aaindex_value (vector <double> & regression_coefficients,  vector <double>                 & predictors )
{
    int reg_coeff_num = regression_coefficients.size();

    double value = 0.0;
    for (int ii=0;  ii  <   reg_coeff_num   -   1;  ii++)
        value += predictors[ii]*regression_coefficients[ii];

    value += regression_coefficients[ reg_coeff_num-1   ];

    return value ;
}

double handle_dummy_FAUJ880111 (string & Isomeric)
{
     vector <string> dummy_positive = {"+"};
     vector <string> dummy_negative = {"-"};;

     int positive_number    = number_of_appearances_of_key (Isomeric,dummy_positive);
     int negative_number    = number_of_appearances_of_key (Isomeric,dummy_negative);

     if ( positive_number > negative_number)
        return 1.0;
     else
        return 0.0;
}


int main(int argc,char  **argv)
{

/// Here you need to process the command line argument. It is further assumed that the argument is acceptable
    string SMILES (argv[1]);
    bool is_valid = true;
    string current_stop_word;
    for (int ii=0;ii<stop_words.size();ii++)
    {
         if ( SMILES.find(stop_words [ii])  !=  std::string::npos )
         {
            current_stop_word = stop_words [ii];
            is_valid = false;
            break;
         }
    }
    if ( ! is_valid )
    {
        cout << "ERROR: Can't calculate properties. Incorrect SMILES component: " << current_stop_word << endl;
        exit(-1);
    }

    vector <double> predictors;

    mk_predictor_by_SMILES (
        SMILES,
        predictors);

   for(auto x: map_aaindex_ID_to_regression_parm)
   {
      double poperty_value = calculate_aaindex_value (x.second,  predictors ) ;
      cout << x.first << "\t" << poperty_value << endl;
   }
   cout <<"FAUJ880111" <<  "\t" << handle_dummy_FAUJ880111 (SMILES)<< endl;
}
