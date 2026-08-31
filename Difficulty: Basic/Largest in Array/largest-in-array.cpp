class Solution {
  public:
    int largest(vector<int> &arr) {
        // code here
        int ans = arr[0];
        for(int i =1; i< arr.size(); i++){
            if(arr[i] > ans){
                ans = arr[i];
            }
        }
        return ans;
    }
};
